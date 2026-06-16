import os
import sys
import json
import datetime

# Add the root project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.config import load_config
from src.mcp_clients.play_store_client import PlayStoreClient
from src.core.normalizer import ReviewNormalizer

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def main():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "settings.yaml")
    config = load_config(config_path)
    
    app_id = "com.nextbillion.groww" # Correct Play Store app ID for Groww
    client = PlayStoreClient(app_id=app_id)
    
    # 1. Fetch raw reviews
    raw_reviews = client.fetch_reviews(weeks=config.time_window_weeks)
    
    # Define cache directories based on today's date
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache", "groww", today_str)
    os.makedirs(cache_dir, exist_ok=True)
    
    raw_path = os.path.join(cache_dir, "reviews_raw.json")
    norm_path = os.path.join(cache_dir, "reviews_normalized.json")
    
    # 2. Save raw cache
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(raw_reviews, f, indent=2, default=json_serial)
    print(f"Saved {len(raw_reviews)} raw reviews to {raw_path}")
        
    # 3. Normalize
    normalized_reviews = ReviewNormalizer.normalize(raw_reviews)
    
    # 4. Save normalized cache
    with open(norm_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_reviews, f, indent=2)
    print(f"Saved {len(normalized_reviews)} normalized reviews to {norm_path}")

if __name__ == "__main__":
    main()
