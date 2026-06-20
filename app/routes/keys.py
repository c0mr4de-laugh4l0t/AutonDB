from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user
from app.db.vault import store_secret, fetch_secret, delete_secret
from app.db.metadata import store_metadata, delete_metadata

router = APIRouter()

class StoreKeyRequest(BaseModel):
    name: str
    service: str
    tags: list[str] = []
    value: str

@router.post("/store")
def store_key(req: StoreKeyRequest, user=Depends(get_current_user)):
    record_id = store_secret(owner=user["sub"], value=req.value)
    store_metadata(
        record_id=record_id,
        name=req.name,
        service=req.service,
        tags=req.tags,
        owner=user["sub"]
    )
    return {"id": record_id, "message": "Key stored"}

@router.get("/fetch/{record_id}")
def fetch_key(record_id: str, user=Depends(get_current_user)):
    value = fetch_secret(record_id=record_id, owner=user["sub"])
    if not value:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"id": record_id, "value": value}

@router.delete("/delete/{record_id}")
def delete_key(record_id: str, user=Depends(get_current_user)):
    ok = delete_secret(record_id=record_id, owner=user["sub"])
    if not ok:
        raise HTTPException(status_code=404, detail="Key not found")
    delete_metadata(record_id)
    return {"message": "Key deleted"}
