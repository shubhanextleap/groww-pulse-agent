import uuid

class MockPlayStoreClient:
    def fetch_reviews(self, product: str, weeks: int) -> list:
        print(f"MockPlayStoreClient: Fetching reviews for {product} over the last {weeks} weeks...")
        # Return dummy JSON reviews
        return [
            {"id": "1", "rating": 5, "text": "Great app, highly recommend!"},
            {"id": "2", "rating": 2, "text": "App crashes during market open."},
            {"id": "3", "rating": 4, "text": "Good UI, but support is slow."}
        ]

class MockGoogleDocsClient:
    def append_section(self, product: str, content: str) -> str:
        print(f"MockGoogleDocsClient: Appending report to {product} Weekly Pulse Doc...")
        # Return a fake heading link
        heading_id = str(uuid.uuid4())[:8]
        return f"https://docs.google.com/document/d/mock-doc-id/edit#heading=h.{heading_id}"

class MockGmailClient:
    def send_email(self, recipients: list, subject: str, body: str) -> str:
        print(f"MockGmailClient: Sending email to {len(recipients)} recipients...")
        # Return a fake message ID
        message_id = f"msg-{str(uuid.uuid4())[:12]}"
        return message_id
