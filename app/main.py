from fastapi import FastAPI
from app.routers.wallets import router as wallet_router
from app.routers.users import router as user_router


app = FastAPI()
app.include_router(wallet_router)
app.include_router(user_router)


@app.get("/ping")
async def server_check():
    """
    Health check endpoint.
    Returns the status of the server to ensure it's running correctly.
    """
    return {"status": "successful"}