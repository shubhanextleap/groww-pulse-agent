import requests

import os

class GoogleWorkspaceClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.environ.get("MCP_BASE_URL", "http://127.0.0.1:8000")

    def append_to_doc(self, doc_id: str, content: str) -> dict:
        print(f"GoogleWorkspaceClient: Appending report to document {doc_id}...")
        url = f"{self.base_url}/append_to_doc"
        payload = {
            "doc_id": doc_id,
            "content": content
        }
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()

    def create_email_draft(self, to_email: str, subject: str, body: str) -> dict:
        print(f"GoogleWorkspaceClient: Sending email draft to {to_email}...")
        url = f"{self.base_url}/create_email_draft"
        payload = {
            "to": to_email,
            "subject": subject,
            "body": body
        }
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
