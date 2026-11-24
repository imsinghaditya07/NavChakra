# Agent37 Operational Jobs & Prompt Templates

This directory contains prompt templates for recurring or triggered agent jobs powered by Agent37.

## IMPORTANT SCHEDULING RULE
> **DO NOT CREATE SCHEDULES AUTOMATICALLY.**
> Schedules on Agent37 consume persistent runtime / compute budget and should only be configured intentionally by human system administrators via the Agent37 dashboard or explicit cron triggers.

---

## Included Job Templates

### 1. `daily_bilingual_bulletin.txt`
- **Purpose**: Generates a daily morning agromet weather and sowing advisory bulletin in both English and Hindi.
- **Data Source**: Fetches live block state from NavChakra `/api/agent-tools/forecast/{block_id}` and `/api/agent-tools/alerts`.
- **Output**: Formatted WhatsApp / SMS / Web bulletin snippet.
- **Manual Execution via Agent37 API**:
  ```bash
  curl -X POST "$AGENT37_INSTANCE_URL/v1/responses" \
    -H "X-Agent37-Key: $AGENT37_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "input": "'"$(cat backend/app/agents/jobs/daily_bilingual_bulletin.txt)"'"
    }'
  ```

### 2. `health_report.txt`
- **Purpose**: Performs an agentic audit of model drift, active warnings, and crowd override frequency.
- **Data Source**: Fetches from `/api/health/model` and `/api/agent-tools/crowd-reports`.
- **Output**: Markdown summary report highlighting any model accuracy degradation or anomalous weather patterns.
- **Manual Execution via Agent37 API**:
  ```bash
  curl -X POST "$AGENT37_INSTANCE_URL/v1/responses" \
    -H "X-Agent37-Key: $AGENT37_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "input": "'"$(cat backend/app/agents/jobs/health_report.txt)"'"
    }'
  ```
