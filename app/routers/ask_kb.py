from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter(prefix="/ask-kb", tags=["ask-kb"])
client = OpenAI()

SYSTEM = (
    "Sei un assistente che risponde SOLO in base ai documenti indicizzati. "
    "Se l’informazione non è presente, di' che non è nel contesto. "
    "Includi citazioni concise (nome file e, se presente, pagina). Rispondi in italiano."
)

@router.post("")
def ask_kb(payload: Dict[str, Any]):
    q = payload.get("question")
    model = payload.get("model", "gpt-4o-mini")
    vs_id = os.getenv("OPENAI_VECTOR_STORE_ID")
    if not q:
        raise HTTPException(400, "Missing 'question'")
    if not vs_id:
        raise HTTPException(400, "OPENAI_VECTOR_STORE_ID non impostato. Inizializza KB e carica file prima.")

    resp = client.responses.create(
        model=model,
        input=q,                  
        instructions=SYSTEM,      
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vs_id]   
            # "max_num_results": 6        
        }],
        # tool_choice="auto",           
    )

    text = getattr(resp, "output_text", "") or ""
    return {"answer": text, "model": model}
