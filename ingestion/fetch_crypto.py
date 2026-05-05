# ingestion/fetch_crypto.py

import requests
import json
import os
from datetime import datetime, timezone

BASE_URL = "https://api.coingecko.com/api/v3"

def fetch_top_coins(vs_currency: str = "usd", per_page: int = 100) -> list[dict]:
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()   # raises error if API call fails

    coins = []
    for coin in response.json():
        coins.append({
            "id": coin.get("id"),
            "symbol": coin.get("symbol"),
            "name": coin.get("name"),
            "current_price": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "market_cap_rank": coin.get("market_cap_rank"),
            "total_volume": coin.get("total_volume"),
            "high_24h": coin.get("high_24h"),
            "low_24h": coin.get("low_24h"),
            "price_change_24h": coin.get("price_change_24h"),
            "price_change_percentage_1h": coin.get("price_change_percentage_1h_in_currency"),
            "price_change_percentage_24h": coin.get("price_change_percentage_24h_in_currency"),
            "price_change_percentage_7d": coin.get("price_change_percentage_7d_in_currency"),
            "circulating_supply": coin.get("circulating_supply"),
            "ath": coin.get("ath"),                        # all time high
            "ath_change_percentage": coin.get("ath_change_percentage"),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })

    return coins

def save_to_json(data: list[dict]) -> str:
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/crypto_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved {len(data)} coins to {filename}")
    return filename

if __name__ == "__main__":
    print("Fetching top 100 coins from CoinGecko...")
    coins = fetch_top_coins()
    save_to_json(coins)