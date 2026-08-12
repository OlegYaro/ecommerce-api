from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health_check():
    """Health check endpoint to verify if the application is running."""
    return {"status": "healthy"}
