from src.core.config import ConfigSchema
from src.mcp_clients.mock_clients import MockPlayStoreClient
from src.mcp_clients.remote_client import GoogleWorkspaceClient
from src.core.clustering import ClusteringEngine
from src.core.summarizer import LLMSummarizer
from src.core import audit

import json
import os
import datetime
import traceback
from dotenv import load_dotenv

load_dotenv()

class ReviewPulseAgent:
    def __init__(self, config: ConfigSchema):
        self.config = config
        self.workspace_client = GoogleWorkspaceClient()
        self.cluster_engine = ClusteringEngine()
        self.summarizer = LLMSummarizer()

    def run(self, force: bool = False):
        iso_week = audit.get_current_iso_week()
        if not force and audit.has_run_for_week(self.config.target_product, iso_week):
            print(f"Agent: Idempotency check failed. Already ran for {iso_week}. Use --force to override.")
            return

        try:
            self._execute_pipeline(iso_week)
        except Exception as e:
            error_msg = f"Pipeline failed: {e}\n{traceback.format_exc()}"
            print(f"Agent: {error_msg}")
            
            error_email = os.environ.get("ERROR_EMAIL_TO")
            if error_email:
                print(f"Agent: Sending error notification to {error_email}...")
                try:
                    self.workspace_client.create_email_draft(
                        error_email,
                        f"[ERROR] Review Pulse Pipeline Failed: {self.config.target_product}",
                        error_msg
                    )
                except Exception as email_err:
                    print(f"Agent: Failed to send error email. {email_err}")

    def _execute_pipeline(self, iso_week: str):
        print("=== Starting Weekly Product Review Pulse ===")
        print(f"Target Product: {self.config.target_product}")
        print(f"Time Window: {self.config.time_window_weeks} weeks")
        
        # In Phase 2b, we assume Phase 2a has already run and populated the cache
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        cache_path = os.path.join("data", "cache", "groww", today_str, "reviews_normalized.json")
        
        if not os.path.exists(cache_path):
            print(f"Agent: Normalized cache not found at {cache_path}. Run Phase 2a first!")
            return
            
        with open(cache_path, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
            
        print(f"Agent: Loaded {len(reviews)} normalized reviews from cache.")

        # 2b. Reasoning Engine
        print("Agent: Phase 2b - Running Embeddings & Clustering...")
        clusters = self.cluster_engine.cluster_reviews(reviews)
        
        print("Agent: Phase 2b - Running LLM Summarization...")
        json_report_str = self.summarizer.process_all_clusters(clusters)
        
        try:
            report_dict = json.loads(json_report_str)
        except Exception as e:
            print(f"Agent: Failed to parse JSON from LLM: {e}")
            report_dict = {"top_themes": ["Error generating themes"], "user_quotes": [], "action_ideas": []}

        # Convert to nice markdown for Docs/Email
        final_report_md = "## Groww Weekly Pulse\n\n"
        final_report_md += "### Top Themes\n"
        for t in report_dict.get("top_themes", []):
            final_report_md += f"- {t}\n"
        
        final_report_md += "\n### Real User Quotes\n"
        for q in report_dict.get("user_quotes", []):
            final_report_md += f"> \"{q}\"\n\n"
            
        final_report_md += "### Action Ideas\n"
        for a in report_dict.get("action_ideas", []):
            final_report_md += f"- {a}\n"
        
        # Save report locally as well
        with open("final_report.md", "w", encoding="utf-8") as f:
            f.write(final_report_md)
            
        latest_report = {
            "product": self.config.target_product,
            "iso_week": iso_week,
            "timestamp": datetime.datetime.now().isoformat(),
            "content": final_report_md,
            "report_data": report_dict
        }
        
        report_json_path = os.path.join("data", "latest_report.json")
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(latest_report, f, indent=2)
            
        print("Agent: Report saved locally to final_report.md and data/latest_report.json")

        # 3. Publish to Docs
        print("Agent: Phase 3 - Output Delivery (Skipping MCP connection locally)")
        doc_res = {}
        msg_res_list = []
        
        # 5. Auditing
        audit.log_successful_run(self.config.target_product, iso_week, doc_res, msg_res_list)
        print("=== Run Complete ===")
