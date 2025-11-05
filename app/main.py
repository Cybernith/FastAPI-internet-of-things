from fastapi import FastAPI

app = FastAPI(title="FastAPI internet of things")

@app.get("/health")
def health():
    return {"status": "health check successfully done"}

