import re

class ReviewNormalizer:
    @staticmethod
    def is_english_and_emoji_free(text: str) -> bool:
        # Check if the string contains mostly ASCII (simple English check)
        # and doesn't contain emojis (non-ASCII high range)
        # A simple check: if all characters are within ASCII range 0-127
        # It's strict, but ensures no emojis and pure English text.
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
        return True

    @staticmethod
    def normalize(raw_reviews: list) -> list:
        normalized = []
        for r in raw_reviews:
            content = r.get('content', '')
            
            # 1. Rule: Must have 8 or more words
            words = content.split()
            if len(words) < 8:
                continue
                
            # 2. Rule: English and no emojis
            if not ReviewNormalizer.is_english_and_emoji_free(content):
                continue
                
            # 3. Rule: Strip out specified metadata.
            # Only keeping score and content
            clean_review = {
                "score": r.get('score'),
                "content": content
            }
            normalized.append(clean_review)
            
        print(f"Normalizer: Kept {len(normalized)} reviews out of {len(raw_reviews)}.")
        return normalized
