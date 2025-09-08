from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse
from app.openai_client import client
from app.utils.backoff import openai_retry

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
@openai_retry()
def chat(req: ChatRequest):
    resp = client.chat.completions.create(
        model=req.model,
        messages=[m.model_dump() for m in req.messages],
        temperature=req.temperature,
        max_tokens=req.max_output_tokens
    )
    choice = resp.choices[0].message
    usage = resp.usage
    return ChatResponse(
        content=choice.content or "",
        model=resp.model,
        prompt_tokens=getattr(usage, "prompt_tokens", 0),
        completion_tokens=getattr(usage, "completion_tokens", 0),
        total_tokens=getattr(usage, "total_tokens", 0),
    )

@router.post("/stream")
def chat_stream(req: ChatRequest):
    if not req.stream:
        req.stream = True

    def event_gen():
        stream = client.chat.completions.create(
            model=req.model,
            messages=[m.model_dump() for m in req.messages],
            temperature=req.temperature,
            max_tokens=req.max_output_tokens,
            stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield f"data: {delta.content}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
