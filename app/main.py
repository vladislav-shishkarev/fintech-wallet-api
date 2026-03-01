from fastapi import FastAPI
from app.routers.wallets import router as wallet_router


app = FastAPI()
app.include_router(wallet_router)

@app.get("/ping")
async def server_check():
    """
    Health check endpoint.
    Returns the status of the server to ensure it's running correctly.
    """
    return {"status": "successful"}