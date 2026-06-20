from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user
from app.core.resolver import resolve_query
from app.db.vault import fetch_secret

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def query_key(req: QueryRequest, user=Depends(get_current_user)):
    record_id = resolve_query(query=req.query, caller_scope=[user["sub"]])
    if not record_id:
        raise HTTPException(status_code=404, detail="No matching credential found")
    value = fetch_secret(record_id=record_id, owner=user["sub"])
    if not value:
        raise HTTPException(status_code=404, detail="Key not found in vault")
    return {"id": record_id, "value": value}
