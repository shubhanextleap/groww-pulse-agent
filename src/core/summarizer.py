import os
import time
from groq import Groq

class LLMSummarizer:
    def __init__(self):
        # We assume GROQ_API_KEY is loaded in environment via python-dotenv
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in environment!")
            
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"
        
        # Groq Limits for 2b
        self.rpm_limit = 30
        self.tpm_limit = 12000
        
    def estimate_tokens(self, text: str) -> int:
        # Rough estimation: 1 token ~= 4 characters or 0.75 words
        return len(text.split()) * 1.3
        
    def generate_weekly_pulse(self, clusters: dict) -> str:
        # Sample reviews from each cluster to form a representative context
        context_blocks = []
        for c_id, reviews in clusters.items():
            sampled = reviews[:10] # Take up to 10 reviews per cluster
            cluster_text = chr(10).join(f"- {r}" for r in sampled)
            context_blocks.append(f"Theme Group {c_id}:\n{cluster_text}\n")
            
        full_context = "\n".join(context_blocks)
        
        prompt = f"""
        You are a product analytics expert analyzing recent App Store and Play Store reviews for a financial app.
        Below are clusters of related reviews.
        
        REVIEWS:
        {full_context}
        
        Generate a weekly one-page pulse note strictly as a JSON object with the following structure. Estimate some realistic mock metrics (like health_score or volume) based on the sentiment:
        {{
            "leadership_pulse": {{
                "health_score": 85,
                "sentiment": "Positive/Neutral/Negative",
                "top_highlight": "1 sentence on what's going well",
                "key_risk": "1 sentence on the biggest user pain point"
            }},
            "product_insights": [
                {{"issue": "Issue description", "impact": "High/Medium/Low", "action": "Suggested fix to prioritize"}}
            ],
            "support_insights": [
                {{"topic": "Main complaint/query", "volume": "High/Medium/Low", "quote": "Exact user quote here"}}
            ]
        }}
        
        CONSTRAINTS:
        1. Keep the entire response highly scannable. Limit arrays to 3-4 items max.
        2. DO NOT include any PII (no usernames, emails, or IDs). Mask them if present.
        3. Output ONLY the JSON object. No markdown wrapping, no extra text.
        """
        
        estimated_tokens = self.estimate_tokens(prompt)
        print(f"LLMSummarizer: Sending weekly pulse request to Groq ({self.model_name}) - Est Tokens: {estimated_tokens}...")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a product analytics expert that only outputs strict JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            time.sleep(2) 
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            # Fallback JSON structure
            fallback = {
                "leadership_pulse": {"health_score": 0, "sentiment": "Unknown", "top_highlight": "Error", "key_risk": "Error"},
                "product_insights": [],
                "support_insights": []
            }
            import json
            return json.dumps(fallback)

    def process_all_clusters(self, clusters: dict) -> str:
        return self.generate_weekly_pulse(clusters)
