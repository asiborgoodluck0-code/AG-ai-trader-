"""
AG AI TRADER — DEMO PAPER-TRADING API
No broker connection. No real orders. All trades are simulated.
"""
from datetime import datetime, timezone
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import random

app = FastAPI(title="AG AI TRADER Demo API", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo only; restrict to your dashboard domain before production.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

balance = 10000.0
positions = []
history = []
symbols = {"EURUSD": 1.0850, "GBPUSD": 1.2710, "USDJPY": 149.50,
           "XAUUSD": 2350.00, "BTCUSD": 65000.00}

class TradeRequest(BaseModel):
    action: Literal["BUY", "SELL"]
    symbol: Literal["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD"]
    volume: float = Field(ge=0.01, le=0.1)
    stop_loss_points: int = Field(ge=1, le=5000)
    take_profit_points: int = Field(ge=1, le=10000)
    risk_percent: float = Field(gt=0, le=1)
    max_open_trades: int = Field(ge=1, le=3)
    account_type: Literal["Demo"] = "Demo"

class AutoRequest(BaseModel):
    enabled: bool
    symbol: str
    risk_percent: float = Field(gt=0, le=1)

@app.get("/")
def home():
    return {"name": "AG AI TRADER", "mode": "PAPER_TRADING_ONLY",
            "message": "Demo simulator API. No MT5 or broker is connected."}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/api/status")
def status():
    # "connected" means this demo API is responding, NOT that MT5 is connected.
    return {"connected": True, "mt5_connected": False, "mode": "PAPER_TRADING_ONLY",
            "message": "Demo API online. MT5 broker connection is not configured.",
            "account": {"balance": f"${balance:,.2f}",
                        "equity": f"${balance:,.2f}", "positions": len(positions)}}

@app.get("/api/analyse")
def analyse(symbol: str = "EURUSD", timeframe: str = "M15"):
    if symbol not in symbols:
        raise HTTPException(400, "Unsupported symbol.")
    r = random.random()
    if r < .30:
        signal, reason = "BUY", "Simulated upward-momentum example. Not a real market signal."
    elif r < .60:
        signal, reason = "SELL", "Simulated downward-momentum example. Not a real market signal."
    else:
        signal, reason = "WAIT", "No simulated setup passed the demo filter."
    return {"signal": signal, "reason": reason, "symbol": symbol,
            "timeframe": timeframe, "price": symbols[symbol], "mode": "SIMULATED"}

@app.post("/api/trade")
def trade(req: TradeRequest):
    if req.account_type != "Demo":
        raise HTTPException(403, "Only demo/paper trades are allowed.")
    if len(positions) >= req.max_open_trades:
        raise HTTPException(400, "Maximum open demo positions reached.")
    p = {"id": len(history) + len(positions) + 1,
         "time": datetime.now(timezone.utc).isoformat(),
         "symbol": req.symbol, "type": req.action, "volume": req.volume,
         "entry_price": symbols[req.symbol], "stop_loss_points": req.stop_loss_points,
         "take_profit_points": req.take_profit_points, "status": "OPEN",
         "result": "SIMULATED — no real funds"}
    positions.append(p)
    return {"ok": True, "message": f"Paper {req.action} simulated for {req.symbol}; no broker order placed.", "position": p}

@app.post("/api/positions/close-all")
def close_all():
    closed = []
    while positions:
        p = positions.pop(0)
        p["status"] = "CLOSED"
        p["closed_time"] = datetime.now(timezone.utc).isoformat()
        history.insert(0, p)
        closed.append(p)
    return {"ok": True, "message": f"Closed {len(closed)} simulated position(s).", "closed": closed}

@app.get("/api/positions")
def get_positions():
    return {"positions": positions}

@app.get("/api/history")
def get_history():
    return {"history": history[:50]}

@app.post("/api/auto-trading")
def auto_trading(req: AutoRequest):
    if req.enabled:
        raise HTTPException(403, "Automatic execution is disabled in this prototype.")
    return {"ok": True, "enabled": False, "message": "Auto-execution remains disabled."}
