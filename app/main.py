from fastapi import FastAPI

app = FastAPI(
    title="Site Monitor API",
    version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": "Service is running"}