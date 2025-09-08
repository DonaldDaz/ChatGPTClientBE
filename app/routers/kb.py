from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Optional, Dict, Any
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
router = APIRouter(prefix="/kb", tags=["kb"])
client = OpenAI()

ENV_PATH = Path(".env")
ENV_KEY = "OPENAI_VECTOR_STORE_ID"


def get_vector_store_id() -> Optional[str]:
    return os.getenv(ENV_KEY)


def set_vector_store_id(vs_id: str) -> None:
    existing = ENV_PATH.read_text(encoding="utf-8") if ENV_PATH.exists() else ""
    lines, replaced = [], False
    for line in existing.splitlines():
        if line.strip().startswith(f"{ENV_KEY}="):
            lines.append(f"{ENV_KEY}={vs_id}")
            replaced = True
        else:
            lines.append(line)
    if not replaced:
        if existing and not existing.endswith("\n"):
            lines.append("")
        lines.append(f"{ENV_KEY}={vs_id}")
    ENV_PATH.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    os.environ[ENV_KEY] = vs_id


@router.get("/vector-store")
def get_vs() -> Dict[str, Any]:
    return {"vector_store_id": get_vector_store_id()}


@router.post("/vector-store/init")
def init_vector_store(name: str = "my-kb") -> Dict[str, Any]:
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY non presente")
        vs = client.vector_stores.create(name=name)
        set_vector_store_id(vs.id)
        return {"vector_store_id": vs.id, "name": vs.name}
    except Exception as e:
        raise HTTPException(500, f"Init vector store failed: {type(e).__name__}: {e}")


@router.delete("/vector-store")
def delete_vector_store() -> Dict[str, Any]:
    vs_id = get_vector_store_id()
    if not vs_id:
        raise HTTPException(400, "OPENAI_VECTOR_STORE_ID non impostato.")
    client.vector_stores.delete(vs_id)
    os.environ.pop(ENV_KEY, None)
    return {"deleted": True, "vector_store_id": vs_id}


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)) -> Dict[str, Any]:
    vs_id = get_vector_store_id()
    if not vs_id:
        raise HTTPException(400, "Vector store non inizializzato. Chiama /kb/vector-store/init prima.")
    if not files:
        raise HTTPException(400, "Nessun file fornito.")

    uploaded_file_ids: List[str] = []
    for f in files:
        data = await f.read()
        if not data:
            continue
        up = client.files.create(file=(f.filename, data), purpose="assistants")
        uploaded_file_ids.append(up.id)

    batch = client.vector_stores.file_batches.create(
        vector_store_id=vs_id,
        file_ids=uploaded_file_ids
    )
    return {
        "vector_store_id": vs_id,
        "uploaded_file_ids": uploaded_file_ids,
        "batch_status": getattr(batch, "status", "submitted")
    }


@router.get("/files")
def list_files(limit: int = 50) -> Dict[str, Any]:
    vs_id = get_vector_store_id()
    if not vs_id:
        raise HTTPException(400, "Vector store non inizializzato.")
    safe_limit = min(max(limit, 1), 100)

    res = client.vector_stores.files.list(vector_store_id=vs_id, limit=safe_limit)

    items = []
    for assoc in getattr(res, "data", []):
        file_id = getattr(assoc, "file_id", None) or getattr(assoc, "id", None)
        fname = None
        fsize = None
        try:
            if file_id:
                fmeta = client.files.retrieve(file_id)
                fname = getattr(fmeta, "filename", None)
                fsize = getattr(fmeta, "bytes", None)
        except Exception:
            pass

        items.append({
            "id": assoc.id,                 
            "file_id": file_id,             
            "filename": fname,              
            "bytes": fsize,                 
            "created_at": getattr(assoc, "created_at", None),
        })

    return {
        "vector_store_id": vs_id,
        "count": len(items),
        "files": items,
        "has_more": getattr(res, "has_more", False),
    }



@router.delete("/files/{file_id}")
def remove_file(file_id: str) -> Dict[str, Any]:
    vs_id = get_vector_store_id()
    if not vs_id:
        raise HTTPException(400, "Vector store non inizializzato.")
    client.vector_stores.files.delete(vector_store_id=vs_id, file_id=file_id)
    return {"removed": True, "vector_store_id": vs_id, "file_id": file_id}
