# webhook-logs

FastAPI service that receives any JSON payload via `POST /webhook` and forwards it to a Discord channel as a formatted code block.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhook` | Accepts any JSON body, posts to Discord |
| `GET` | `/health` | Returns `{"status": "ok"}` |

## Requirements

- `DISCORD_WEBHOOK_URL` — Discord webhook URL (required at runtime; container fails to start without it)

## Running locally

```bash
cp .env.example .env  # add your DISCORD_WEBHOOK_URL
pip install -r requirements.txt
uvicorn main:app --reload
```

## Running with Docker

```bash
docker pull ghcr.io/roger-dplb/webhook-logs:latest

docker run --rm \
  -e DISCORD_WEBHOOK_URL=<your-discord-webhook-url> \
  -p 8000:8000 \
  ghcr.io/roger-dplb/webhook-logs:latest
```

## CI/CD

Push to `main` automatically builds and pushes the Docker image to GHCR:

- `ghcr.io/roger-dplb/webhook-logs:latest`
- `ghcr.io/roger-dplb/webhook-logs:sha-<short-sha>`
