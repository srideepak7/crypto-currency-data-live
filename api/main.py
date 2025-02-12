from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import requests

app = FastAPI()

API_KEY = "799d534f-7810-42b9-8956-b7581ba1497a"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

PARAMS = {
    "start": "1",
    "limit": "50",
    "convert": "USD"
}

@app.get("/")
def serve_frontend():
    """Serve the frontend HTML page."""
    return FileResponse("static/index.html")

@app.get("/crypto")
def fetch_crypto_data():
    """Fetch live cryptocurrency data and return it as JSON."""
    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        data = response.json()

        crypto_data = []
        for coin in data["data"]:
            crypto_data.append({
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["quote"]["USD"]["price"],
                "market_cap": coin["quote"]["USD"]["market_cap"],
                "volume_24h": coin["quote"]["USD"]["volume_24h"],
                "change_24h": coin["quote"]["USD"]["percent_change_24h"],
            })

        return JSONResponse(content=crypto_data)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
