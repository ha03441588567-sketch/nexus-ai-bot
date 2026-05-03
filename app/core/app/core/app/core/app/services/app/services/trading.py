import httpx
import numpy as np
import logging

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3"

COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "ADA": "cardano",
    "XRP": "ripple",
    "DOGE": "dogecoin",
}

def normalize(coin: str) -> str:
    return COIN_MAP.get(coin.upper(), coin.lower())

async def get_price(coin: str) -> dict:
    coin_id = normalize(coin)
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{COINGECKO_URL}/coins/{coin_id}")
        data = resp.json()
    market = data["market_data"]
    return {
        "name": data["name"],
        "symbol": data["symbol"].upper(),
        "price": market["current_price"]["usd"],
        "change_24h": market["price_change_percentage_24h"],
        "market_cap": market["market_cap"]["usd"],
    }

async def get_prices_history(coin: str) -> list:
    coin_id = normalize(coin)
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{COINGECKO_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": 50}
        )
        data = resp.json()
    return [p[1] for p in data.get("prices", [])]

def calculate_rsi(prices: list) -> float:
    arr = np.array(prices)
    deltas = np.diff(arr)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[:14])
    avg_loss = np.mean(losses[:14])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

async def get_signal(coin: str) -> dict:
    price_data = await get_price(coin)
    prices = await get_prices_history(coin)
    rsi = calculate_rsi(prices)
    if rsi < 30:
        signal = "🟢 BUY"
    elif rsi > 70:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"
    return {**price_data, "rsi": rsi, "signal": signal}
