from fastapi import FastAPI

app = FastAPI(title="AI Sales Intelligence API")


@app.get("/health")
def health():
    return {"status": "ok"}