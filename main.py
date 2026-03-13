import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

load_dotenv()

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
DISCORD_MAX_LENGTH = 1990  # Discord limit is 2000; leaving room for wrapper text

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    # Truncate if payload exceeds Discord's message limit
    if len(formatted) > DISCORD_MAX_LENGTH:
        formatted = formatted[:DISCORD_MAX_LENGTH] + "\n... (truncated)"

    message = f"🚨 **Webhook Log**\n```json\n{formatted}\n```"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
        )

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=502,
            detail=f"Discord returned {response.status_code}: {response.text}",
        )

    return {"ok": True}
