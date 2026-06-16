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
        
    def summarize_cluster(self, cluster_id: int, reviews: list) -> str:
        if cluster_id == -1:
            theme_hint = "Miscellaneous / Outliers"
        else:
            theme_hint = f"Cluster {cluster_id}"
            
        prompt = f"""
        You are analyzing user reviews for a financial app. Here is a cluster of similar reviews.
        Theme: {theme_hint}
        
        Reviews:
        {chr(10).join(f"- {r}" for r in reviews)}
        
        Please provide the following as plain, unformatted text (do NOT use markdown, bolding, asterisks, or hash symbols):
        1. Top Theme: A concise 3-5 word name for this cluster's theme.
        2. Real User Quote: Extract exactly one highly representative, verbatim quote from the text above.
        3. Action Idea: One sentence suggesting how product/support can address this.
        """
        
        # Rate Limit Protection
        estimated_tokens = self.estimate_tokens(prompt)
        if estimated_tokens > self.tpm_limit:
            print(f"WARNING: Chunk exceeds TPM limit ({estimated_tokens} tokens). Truncating...")
            # Naive truncation for safety
            prompt = prompt[:int(self.tpm_limit * 3)] 

        print(f"LLMSummarizer: Sending request to Groq ({self.model_name}) - Est Tokens: {estimated_tokens}...")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a product analytics expert."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.3,
            )
            # Enforce strict 30 RPM limit locally (2s wait per request)
            time.sleep(2) 
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return "Error generating summary."

    def process_all_clusters(self, clusters: dict) -> str:
        final_report = "Weekly Pulse Summary\n\n"
        for c_id, reviews in clusters.items():
            if len(reviews) < 2 and c_id != -1:
                continue # Skip tiny clusters unless it's noise
                
            # If a cluster is too big, chunk it to avoid hitting 12K TPM
            # For simplicity in this implementation, we take a random sample of max 50 reviews per cluster
            sampled_reviews = reviews[:50] 
            
            summary = self.summarize_cluster(c_id, sampled_reviews)
            final_report += f"{summary}\n\n"
            
        return final_report
