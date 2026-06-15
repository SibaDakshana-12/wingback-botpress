# Design Document

## 1. Problem statement

AI security platforms need to evaluate third-party AI agents (chatbots,
copilots, assistants) for vulnerabilities such as prompt injection, PII
leakage, and jailbreaks. Each SaaS AI platform (Botpress, Decagon,
Copilot Studio, Agentforce, etc.) exposes a different API, so a
connector layer abstracts platform-specific details behind a common
`validate_target()` / `execute_test()` interface, allowing the scanning
engine to remain platform-agnostic.

## 2. Architecture

UI (React) --> Backend API (FastAPI) --> BotpressScanner --> Botpress Chat API

|

SQLite (resources, scans)

The UI calls REST endpoints under `/api/v1`. The backend persists
onboarded resources and scan history, and delegates all Botpress
communication to `BotpressScanner`.

## 3. Onboarding model

Fields captured: `account_name`, `resource_name`, `webhook_id`
(required), `encryption_key`, `user_id`, `description` (optional).
`encryption_key` is stored but redacted (`***redacted***`) in all API
responses. Validation rules: `account_name`, `resource_name`, and
`webhook_id` are required non-empty strings.

## 4. Botpress integration

- **Connect**: creates a chat user via `POST /users`, optionally with
  manual auth (`encryption_key` + `user_id`) if configured.
- **Converse**: `POST /conversations` to create a conversation,
  `POST /messages` to send the adversarial prompt.
- **Receive reply**: polling via `GET /conversations/{id}/messages`,
  sorted by `createdAt`, looking for the first message after the sent
  message ID.

**SSE vs poll**: polling was chosen for simplicity in a short-lived
request/worker context — no persistent connection management, easy to
mock in tests, and acceptable given low free-tier message volume. SSE
(`listenConversation`) would reduce latency in production.

## 5. Conversation lifecycle

By default, a scan reuses the active conversation across prompts within
a single scan call unless `reset_conversation: true` is passed (the UI
defaults this to checked), which starts a fresh conversation —
providing test isolation between scan runs.

## 6. Error handling matrix

| Botpress HTTP status | User-visible message |
|---|---|
| 401 / 403 | Authentication failed — check credentials |
| 404 | Target not found — check webhook ID |
| 429 | Rate limited — try again later |
| 5xx | Botpress service error — try again later |
| timeout | Bot did not respond within the configured timeout |

All error messages are sanitized — no encryption keys, user keys, or
stack traces are surfaced to the UI or API consumer.

## 7. Security

- `encryption_key` is stored in SQLite but redacted in every API
  response.
- `webhook_id` is a path segment appended to a fixed base URL
  (`https://chat.botpress.cloud/{webhook_id}`), not a free-form URL —
  this prevents SSRF via arbitrary user-supplied URLs.
- Logs and error messages never include secrets (verified via unit
  tests).
- No authentication is implemented for this demo; all endpoints are
  open, as stated in `README.md`.

## 8. Observability

In production, this service would emit structured logs per scan
(resource ID, vulnerability/attack IDs, latency, success/error code)
and metrics (scan count, error rate by category, p50/p95 latency per
platform) to support alerting on elevated failure rates.

## 9. Testing strategy

- **Unit tests** (`tests/test_scanner.py`): connector logic against an
  injected `BotpressChatClient` backed by `httpx.MockTransport`, no
  real network calls. Covers validation success/failure, happy path,
  timeout, rate limiting, conversation reset, secret redaction, and
  text extraction.
- **Integration tests** (`tests/test_api.py`): full REST API exercised
  via FastAPI's `TestClient` against an isolated in-memory SQLite DB,
  with the scanner's HTTP client patched to a mock Botpress server.
- **Live smoke test**: manual steps documented in `README.md` against
  a real Botpress bot.

CI does not depend on live Botpress credentials — all automated tests
run against mocks.

## 10. Production hardening

- Multi-tenant: scope resources by account/org ID, add row-level
  authorization.
- Feature flags: gate new connector platforms or delivery modes (SSE)
  behind flags for gradual rollout.
- Backward compatibility: version the `/api/v1` prefix; add `/api/v2`
  for breaking changes rather than mutating v1 contracts.
- Rate limiting: apply per-resource scan rate limits to avoid burning
  a customer's Botpress message quota.

## 11. Known limitations

- Free-tier Botpress message caps (~500/month).
- Only `text` payload types are parsed for bot responses; rich message
  types (image, carousel, etc.) return `model_response: null`.
- Polling-based reply delivery only; SSE not implemented.
- SQLite persistence — suitable for demo scale, not multi-instance
  deployments.