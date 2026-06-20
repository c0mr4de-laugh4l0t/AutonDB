from fastapi import FastAPI
from app.routes import keys, query, auth
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AutonDB", version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(keys.router, prefix="/keys", tags=["keys"])
app.include_router(query.router, prefix="/query", tags=["query"])

@app.get("/health")
def health():
    return {"status": "ok"}
