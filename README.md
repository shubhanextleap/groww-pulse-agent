# Groww Pulse AI Agent 📈

An autonomous AI Agent designed to automatically scrape, cluster, and summarize weekly user feedback for the Groww Play Store application. It orchestrates multiple LLMs to generate a crisp "Weekly Pulse" report, pushes it to Google Docs, drafts it in Gmail, and serves it on a beautiful Streamlit web dashboard.

## 🌟 Architecture

1. **Scraping Engine**: Fetches the latest reviews from the Google Play Store using the `google-play-scraper`.
2. **Clustering Engine**: Uses SentenceTransformers and K-Means to semantically group feedback into actionable themes (e.g., Bugs, Feature Requests, Praise).
3. **LLM Summarization**: Leverages the Groq API (Llama 3) to generate human-readable, executive summaries of each cluster.
4. **Delivery Layer**: Connects to a custom MCP (Model Context Protocol) Server to autonomously append the report to a Google Doc and draft an email to stakeholders.
5. **Interactive Dashboard**: A Streamlit web application that provides a beautiful, shareable UI for the weekly report.

## 🚀 Deployment (Railway)

This repository is configured to be deployed easily on [Railway.app](https://railway.app/). 

The included `Procfile` and `start.sh` script ensure that both the Streamlit Dashboard (`web`) and the background Scheduler (`worker`) run seamlessly in a single unified container, sharing the same filesystem for data syncing.

### 1. Connect GitHub
1. Create a new project in Railway.
2. Select **Deploy from GitHub repo** and select this repository.

### 2. Configure Environment Variables
Because `.env` files are strictly excluded from source control for security, Railway will start completely blank. You **must** define the following variables in the **Variables** tab of your Railway project:

- `GROQ_API_KEY`: Your API key from the Groq Console (Required for LLM summarization).
- `MCP_API_SECRET_KEY`: The authentication secret used to connect to your remote MCP server.
- `GOOGLE_DOC_ID`: The ID of the target Google Doc where reports should be appended.
- `PULSE_EMAIL_TO`: The email address of the stakeholder receiving the report.
- `PULSE_EMAIL_MODE`: Set to `draft` to create drafts, or `send` to send immediately.
- `ERROR_EMAIL_TO`: The email address that should receive stack traces if the background job fails.

*(Note: See `.env.example` for the variable keys, but never commit your actual keys).*

### 3. Setup the Remote MCP Server
This AI Agent requires a remote **Google Workspace MCP Server** to handle appending the reports to Google Docs and drafting the notification emails.

1. Create a separate GitHub repository for your MCP Server (built using FastAPI and Google API credentials).
2. Deploy the MCP Server to Railway just like you did with the AI Agent.
3. In your MCP Server's Railway variables, define your `GOOGLE_CREDENTIALS` (as a JSON string) and an `API_SECRET_KEY` for authentication.
4. Go back to your **AI Agent's** Railway variables and add `MCP_BASE_URL` pointing to the public URL of your deployed MCP server (e.g., `https://your-mcp-server.up.railway.app`). This tells the AI Agent exactly where to send the final reports!

### 4. Access the Dashboard
Once Railway finishes building both services, anyone with the AI Agent's public URL can access the Streamlit dashboard to view the latest automatically generated weekly report!

## 💻 Running Locally

If you wish to test the AI Agent locally on your machine:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup your environment:**
   Create a `.env` file in the root directory and populate it with the variables listed above.
3. **Run the Dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```
4. **Run a Manual Pipeline Test (Dry Run):**
   ```bash
   python scheduler.py --test
   ```

---
*Generated autonomously by Antigravity AI.*
