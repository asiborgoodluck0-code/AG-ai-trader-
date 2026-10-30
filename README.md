# AG AI TRADER — Render deployment package

## Safety and scope
This package is a **paper-trading demo only**. It does not connect to MetaTrader 5,
a broker, or an exchange. Prices and signals are illustrative/simulated. It cannot
place real orders or move real money. Automatic execution is intentionally disabled.

## Deploy from an Android phone
1. Download and unzip this folder.
2. Create a GitHub repository (ask a parent/guardian to help with accounts if needed).
3. Upload `main.py`, `requirements.txt`, and `render.yaml` into the repository root.
4. In Render, create a new Blueprint or Web Service connected to that GitHub repository.
5. Render uses `render.yaml`. If configuring manually, choose Python and use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. After deployment, open `https://YOUR-SERVICE.onrender.com/health` and check for `{"ok":true}`.
7. In the AG AI TRADER dashboard, paste `https://YOUR-SERVICE.onrender.com` into
   "Your secure backend URL", choose Demo, and connect. The dashboard should say
   backend online / demo mode — it is NOT an MT5 connection.

Render free web services may spin down after inactivity and take time to wake up.
Check Render's current pricing and limits before deploying.

## API
- `GET /health`
- `GET /api/status`
- `GET /api/analyse?symbol=EURUSD&timeframe=M15`
- `POST /api/trade` (paper trade only; Demo account required)
- `POST /api/positions/close-all` (closes simulated positions)
- `GET /api/positions`
- `GET /api/history`
- `POST /api/auto-trading` (rejects enabling automation)

## Future MT5 work
A real MT5 integration needs an eligible account holder, broker permission, a compatible
desktop MT5 terminal (commonly Windows), server-side credentials, HTTPS, authentication,
restricted CORS, persistent storage, audit logs, order validation, risk limits and an
emergency stop. Never put broker passwords, account credentials or API keys in HTML,
GitHub, screenshots or chat. Use a demo account and adult supervision for any future testing.
