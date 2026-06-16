# Edge Cases & Corner Cases: Weekly Product Review Pulse

This document outlines potential edge cases and corner cases for the Weekly Product Review Pulse system, categorized by the phase of the pipeline. Addressing these scenarios will ensure the system remains robust and reliable.

## 1. Data Ingestion (Play Store Reviews MCP Server)
- **Zero Reviews Found:** The scraper returns 0 reviews for the 8–12 week window. (Could be due to a bug, network issue, or Google Play HTML structure changes).
- **Rate Limiting / IP Blocking:** Google Play blocks the scraper's IP address due to high frequency or volume of requests.
- **Review Volume Spike:** A sudden massive influx of reviews (e.g., due to an app outage) exceeds memory limits or the LLM context window limits.
- **Language & Encoding Issues:** Reviews submitted in non-English languages, mixed languages, or containing complex emojis/zalgo text that break the embedding model.
- **Extremely Long Reviews:** Users copy-pasting massive blocks of text that exceed the token limits for the embedding or LLM models.

## 2. Reasoning & Processing Engine
- **Quote Hallucination Check Fails:** The LLM generates a highly relevant quote, but it cannot be strictly matched to the source text during the validation phase.
- **Clustering Anomalies (Noise):** HDBSCAN classifies too many reviews as "noise" (label -1), leaving very few reviews for actual theme generation. Alternatively, all reviews get lumped into a single generic cluster.
- **PII Scrubber Bypass:** A user obfuscates their PII (e.g., "call me at nine 9 eight 7...") or includes sensitive financial data that the PII scrubber misses before it hits the LLM.
- **LLM Provider Outage / Timeout:** The LLM API (used for summarization and theme naming) times out, returns a 50x error, or hits rate limits mid-processing.

## 3. Output Delivery (Google Workspace MCP Servers)
- **Partial Delivery Failure:** The system successfully appends the report to the Google Doc, but the Gmail MCP server crashes before sending the email. (The idempotency system must handle this gracefully without appending to the Doc twice on retry).
- **Google Doc Unavailable:** The target "master" Google Doc is deleted, moved, or its sharing permissions are revoked, causing the Google Docs MCP Server to return a 404/403 error.
- **Document Size Limits:** Over months or years, the master Google Doc becomes too large, hitting Google's document size limits or causing the Docs API to time out during the append operation.
- **Invalid Email Recipients:** One or more stakeholder email addresses in the configuration are invalid, causing the Gmail API to reject the entire batch.

## 4. Scheduling, State, and Idempotency
- **Concurrent Runs:** A cron misconfiguration or manual trigger causes two instances of the agent to run for the exact same product and ISO week simultaneously, leading to race conditions.
- **Mid-Run Crash:** The server or agent crashes unexpectedly (e.g., out of memory) in the middle of processing. The system must know whether to restart from scratch or resume upon the next boot.
- **Timezone / DST Shifts:** The "Monday morning IST" trigger fires at the wrong time or skips a run due to server timezone changes or Daylight Saving Time adjustments (if the server is in a locale that observes it).
- **Stale Backfills:** A user tries to CLI-backfill an ISO week from 2 years ago, but the Play Store scraper cannot fetch data that far back due to pagination limits.
