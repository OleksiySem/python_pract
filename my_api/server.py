from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
import httpx

app = FastAPI()

API_KEY_NAME = "X-API-Key"
API_KEY = "supersecret"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def find_coingecko_id(symbol: str):

    for suffix in ["USDT", "BUSD", "USD", "USDC"]:
        if symbol.endswith(suffix):
            base_asset = symbol.removesuffix(suffix).lower()
            break
    else:
        raise HTTPException(status_code=400, detail="Unsupported symbol format")

    search_url = f"https://api.coingecko.com/api/v3/search?query={base_asset}"
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error querying CoinGecko")

    data = response.json()
    for coin in data.get("coins", []):
        if coin["symbol"].lower() == base_asset:
            return coin["id"]

    raise HTTPException(status_code=400, detail="CoinGecko ID not found for this symbol")


@app.get("/crypto-price", dependencies=[Depends(verify_api_key)])
async def get_crypto_price(symbol: str = "BTCUSDT"):
    symbol = symbol.upper()


    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    async with httpx.AsyncClient() as client:
        binance_response = await client.get(binance_url)

    if binance_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid symbol or Binance error")

    binance_data = binance_response.json()
    price = binance_data["price"]

    coin_id = await find_coingecko_id(symbol)

    coingecko_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    async with httpx.AsyncClient() as client:
        coingecko_response = await client.get(coingecko_url)

    if coingecko_response.status_code != 200:
        raise HTTPException(status_code=400, detail="CoinGecko error")

    coingecko_data = coingecko_response.json()
    market_cap = coingecko_data["market_data"]["market_cap"]["usd"]

    return {
        "symbol": binance_data["symbol"],
        "price": price,
        "market_cap_usd": market_cap
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to Crypto Monitor API"}
