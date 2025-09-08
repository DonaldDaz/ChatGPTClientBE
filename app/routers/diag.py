from fastapi import APIRouter
import sys, os
import openai

router = APIRouter(prefix="/diag", tags=["diag"])

@router.get("/env")
def diag_env():
    return {
        "python_executable": sys.executable,
        "python_version": sys.version,
        "openai_version": openai.__version__,
        "has_vector_stores": hasattr(openai.OpenAI(), "vector_stores"),
        "OPENAI_VECTOR_STORE_ID": os.getenv("OPENAI_VECTOR_STORE_ID"),
        "OPENAI_API_KEY_present": bool(os.getenv("OPENAI_API_KEY")),
    }
