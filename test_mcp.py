import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Extract doc ID from the env file
raw_doc_id = os.environ.get("GOOGLE_DOC_ID", "")
doc_id = raw_doc_id.split("/")[0] if "/" in raw_doc_id else raw_doc_id

print(f"Raw doc ID from env: '{raw_doc_id}'")
print(f"Parsed doc ID: '{doc_id}'")

url = 'http://127.0.0.1:8000/append_to_doc'
payload = {
    'doc_id': doc_id, 
    'content': 'Test from AI Agent! We are verifying the connection.'
}

# The server.py didn't show explicit auth headers, but if there is one we can send it
api_key = os.environ.get("MCP_API_SECRET_KEY")
headers = {"X-API-Key": api_key, "Authorization": f"Bearer {api_key}"} if api_key else {}

print(f"Sending POST to {url}...")
try:
    res = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Request failed: {e}")
