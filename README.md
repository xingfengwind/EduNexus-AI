# EduNexus AI

Browser-based teaching resource platform. Phase 0 establishes the Vue Web client, Java business API and internal Python AI service. No native app is included.

## Documents
- [PRD](docs/PRD.md)
- [Design](docs/design-document.md)
- [Stack](docs/tech-stack.md)
- [Plan](memory-bank/implementation-plan.md)
- [Phase 0 evidence](docs/verification/phase-0.md)

## Development
Frontend: `cd frontend`, `npm ci`, `npm run dev`.
Backend: `cd backend`, `./mvnw.cmd verify` (Docker required for integration tests).
AI: `cd ai-service`, `uv sync --locked`, `uv run pytest`, `uv run uvicorn app.api.health:app --host 127.0.0.1 --port 8000`.
Infrastructure: copy `deploy/.env.example` to `deploy/.env`, replace placeholders locally, then `docker compose --env-file deploy/.env -f deploy/compose.yaml up -d`.

Never put model keys in VITE variables or tracked files. Alibaba Cloud Bailian, the account endpoint and `kimi-k3.1-pro` are configured through backend-only environment variables; the real key remains external. Node/Java/Python versions and incomplete checks are recorded in the evidence document.
