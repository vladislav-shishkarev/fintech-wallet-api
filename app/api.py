from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def server_check():
    """
    Health check endpoint.
    Returns the status of the server to ensure it's running correctly.
    """
    return {"status": "successful"}
