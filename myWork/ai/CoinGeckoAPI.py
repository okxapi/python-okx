import requests
import json
from datetime import datetime, timedelta


class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_btc_price():
        """获取 BTC 实时价格数据"""
        url = f"{CoinGeckoAPI.BASE_URL}/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true"
        }

        response = requests.get(url, params=params)
        data = response.json()

        return {
            "symbol": "BTC",
            "price": data["bitcoin"]["usd"],
            "market_cap": data["bitcoin"]["usd_market_cap"],
            "volume_24h": data["bitcoin"]["usd_24h_vol"],
            "change_24h": data["bitcoin"]["usd_24h_change"],
            "last_updated": datetime.fromtimestamp(data["bitcoin"]["last_updated_at"])
        }

    @staticmethod
    def get_btc_historical_data(days=30):
        """获取 BTC 历史价格数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        url = f"{CoinGeckoAPI.BASE_URL}/coins/bitcoin/market_chart/range"
        params = {
            "vs_currency": "usd",
            "from": start_date.timestamp(),
            "to": end_date.timestamp()
        }

        response = requests.get(url, params=params)
        data = response.json()

        prices = []
        for timestamp, price in data["prices"]:
            date = datetime.fromtimestamp(timestamp / 1000)  # CoinGecko 返回的是毫秒时间戳
            prices.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": price
            })

        return prices