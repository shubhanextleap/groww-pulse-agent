# Phase-Wise Implementation Plan: Weekly Product Review Pulse

This document outlines the step-by-step implementation plan for the Weekly Product Review Pulse system for Groww, based on the defined architecture and problem statement.

## Phase 1: Foundation & Project Setup
**Goal:** Establish the core project structure and basic agent orchestration logic.
- Initialize the project repository.
- Set up the Core Agent framework (the orchestrator).
- Define the configuration schema (product target, execution schedule, recipient lists).
- Implement mock MCP server clients to test the basic execution loop without hitting real endpoints.

## Phase 2a: Data Ingestion (Custom Play Store Reviews MCP Server)
**Goal:** Build the dedicated data ingestion layer for Google Play.
- Create a standalone MCP server specifically for Google Play Reviews.
- **Data Storage:** Save the fetched raw reviews to one file, and the normalized reviews to a separate dedicated file.
- **Normalization:** Implement server-side filtering to:
  - Remove all reviews with fewer than 8 words.
  - Remove all reviews containing emojis or written in languages other than English.
  - Strip unnecessary fields from the payload: `reviewId`, `userName`, `userImage`, `reviewCreatedVersion`, `at`, `replyContent`, and `repliedAt`.
- **Deliverable:** Working Play Store MCP Server returning normalized review data and saving the intermediate files.

## Phase 2b: Reasoning & Processing Engine (LLM via Groq)
**Goal:** Transform raw reviews into actionable insights locally within the agent workflow, strictly adhering to Groq API limits.
- **Data Safety:** Implement a pre-processing step to sanitize and scrub PII from review text.
- **Embeddings & Clustering:** 
  - Integrate a text embedding model to convert reviews into vectors.
  - Implement UMAP + HDBSCAN clustering to group semantically similar feedback.
- **LLM Summarization (Groq `llama-3.3-70b-versatile`):**
  - **Rate Limit Constraints:** 
    - Requests per minute: 30
    - Requests per day: 1K
    - Tokens per minute: 12K
    - Tokens per day: 100K
  - *Implementation:* The agent must include rate-limiting and chunking logic to ensure requests stay under the strict 12K TPM and 30 RPM limits.
  - Build targeted LLM prompts to name the top themes for each cluster.
  - Extract and validate verbatim quotes (ensuring they exist in the source text).
  - Generate actionable product/support ideas.
- **Deliverable:** The agent can take raw reviews and generate the finalized narrative structure as plain, unformatted text (no markdown or HTML), since the Google Docs integration does not support formatting.

## Phase 3: Output Delivery Integration
**Goal:** Connect to the remote Google Workspace MCP server (`web-production-85b327.up.railway.app`) for human-visible delivery.
- **Remote Server Integration:**
  - Configure the client to connect to the remote MCP server at `web-production-85b327.up.railway.app` which handles both Google Docs and Gmail operations.
- **Google Docs Operations:**
  - Append the plain text report to the master "Groww Weekly Pulse" document (skipping rich formatting logic).
  - Capture and return the updated document link.
- **Gmail Operations:**
  - Implement logic to construct the teaser email (bulleted themes + "Read full report" link).
  - Add configuration to support a "draft-only" mode for staging environments.

## Phase 4: Scheduling, Idempotency & Auditing
**Goal:** Ensure the system is robust, safe, and autonomous.
- **Idempotency:** Implement state tracking (e.g., checking existing Doc sections or local logs) to guarantee that re-running a specific ISO week does not result in duplicate Doc sections or duplicate emails.
- **Auditing:** Log essential run metadata (Doc heading ID, Gmail message ID, processed review count, LLM cost/tokens used) to a local audit log.
- **Scheduling:** Set up the weekly trigger (e.g., via cron or a cloud scheduler) to run every Monday morning IST, including a CLI for manual backfills.

## Phase 5: End-to-End Testing & Deployment
**Goal:** Validate the full pipeline and transition to production.
- Perform end-to-end dry runs using the Gmail "draft-only" mode.
- Validate clustering quality, LLM summarization accuracy, and quote hallucination checks.
- Test error handling and MCP server timeout scenarios.
- Once verified by stakeholders, toggle Gmail to production sending mode.
