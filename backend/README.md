# SitePulse Backend Skeleton

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

WebSocket stream: `ws://localhost:8000/ws/events`
