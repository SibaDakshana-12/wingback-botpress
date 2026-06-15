# Botpress Connector — Red Team Scanner

End-to-end connector + mini platform for red-team scanning a Botpress bot
via the Botpress Chat API, built for the take-home exercise.

## Live demo

- **UI:** https://wingback-botpress-1.onrender.com
- **API base:** https://wingback-botpress.onrender.com
- **Deployed at:** 2026-06-15T19:00:00Z (IST)
- **Notes:** Free-tier Render services may take ~30-50s to wake up on
  first request after idling (cold start).

## Auth

No authentication — all endpoints are open for evaluation.

## Prerequisites

- Python 3.11+
- Node.js 18+

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # if used
uvicorn app.main:app --reload
```

Runs on `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`.

## Configuring WEBHOOK_ID for live demo

1. In Botpress Studio, open your bot → Integrations → Chat → copy the
   Webhook ID.
2. In the UI, click **+ Add Resource**, fill in Account Name, Resource
   Name, and Webhook ID, then click **Validate & Save**.
3. Once validated, open the resource and run a sample scan (e.g.
   "Jailbreak") to test the live flow.

## Live smoke test (manual steps)

1. Open the hosted UI.
2. Click **+ Add Resource**, enter a Botpress webhook ID, click
   **Validate & Save** — should show "Validated".
3. Open the resource detail page, select a sample prompt (e.g.
   "Jailbreak"), click **Run Scan**.
4. Confirm the bot's response appears in Scan History with latency.

## Endpoints

- `GET /health` — liveness
- `GET /ready` — readiness
- `POST /api/v1/resources` — onboard a resource
- `GET /api/v1/resources` — list resources (secrets redacted)
- `GET /api/v1/resources/{id}` — get one resource
- `POST /api/v1/resources/{id}/validate` — validate connection
- `POST /api/v1/resources/{id}/scan` — run scan(s)
- `GET /api/v1/resources/{id}/scans` — scan history

## Known limitations

- Free-tier Botpress message caps (~500/month) — live demo uses a
  handful of calls.
- Only `text` message payloads are parsed for bot responses; rich
  types (image, carousel) are not extracted.
- Delivery mode is polling (`listMessages`); SSE is not implemented.
- SQLite is used for persistence — single-instance, file-based, fine
  for this demo's scale.

## AI assistance disclosure

This project was built with assistance from Claude (Anthropic), used
for code generation, debugging, and documentation, per the exercise's
allowance for AI tool use.