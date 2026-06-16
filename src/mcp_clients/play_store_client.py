import datetime
from google_play_scraper import reviews, Sort

class PlayStoreClient:
    def __init__(self, app_id: str):
        self.app_id = app_id

    def fetch_reviews(self, weeks: int) -> list:
        print(f"PlayStoreClient: Fetching up to {weeks} weeks of reviews for {self.app_id}...")
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=weeks)
        all_reviews = []
        continuation_token = None
        
        # We loop to fetch reviews. Play store paginates via continuation_token.
        # We sort by NEWEST so we can stop when we hit the cutoff date.
        while True:
            result, continuation_token = reviews(
                self.app_id,
                lang='en', 
                country='in', 
                sort=Sort.NEWEST,
                count=199, # Max per request
                continuation_token=continuation_token
            )
            
            if not result:
                break
                
            older_than_cutoff = False
            for r in result:
                if r['at'] < cutoff_date:
                    older_than_cutoff = True
                    break
                all_reviews.append(r)
                
            if older_than_cutoff or not continuation_token:
                break
                
        print(f"PlayStoreClient: Fetched {len(all_reviews)} raw reviews.")
        return all_reviews
