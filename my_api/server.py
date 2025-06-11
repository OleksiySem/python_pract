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


@app.get("/crypto-price", dependencies=[Depends(verify_api_key)])
async def get_crypto_price(symbol: str = "BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid symbol or Binance error")
    
    data = response.json()
    return {
        "Crypto": data["symbol"],
        "Price": data["price"]
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to Crypto Monitor API"}
