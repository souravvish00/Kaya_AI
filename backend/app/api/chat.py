from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from ..database.schemas import ChatRequest, ChatResponse
from ..knowledge.fact_checker import extract_new_knowledge
from ..knowledge.document_store import retrieve_context
from ..llm.inference import generate_response
from ..memory.long_term import load_facts, load_memory, remember_conversation, save_fact
from ..training.dataset_builder import add_training_example
from ..tools.calculator import calculate, looks_like_calculation
from ..tools.math_tutor import answer_grade_12_math, looks_like_grade_12_math

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    message = request.message.strip()

    if looks_like_grade_12_math(message):
        result = answer_grade_12_math(message)
        response = result["response"]
        _persist_learning(message, response, session_id, request.mode, request.save_training, ["math", "grade-12"])
        return ChatResponse(response=response, session_id=session_id, mode=request.mode)

    if looks_like_calculation(message):
        result = calculate(message)
        if result.get("ok"):
            response = f"Answer: {result['result']}"
        else:
            response = f"I could not calculate that: {result.get('error', 'unknown error')}"
        _persist_learning(message, response, session_id, request.mode, request.save_training, ["calculator"])
        return ChatResponse(response=response, session_id=session_id, mode=request.mode)

    documents = retrieve_context(message)
    recent_memory = load_memory()[-8:]
    saved_facts = load_facts()[-12:]
    try:
        response = generate_response(
            message,
            memory=recent_memory,
            facts=[item.get("fact", "") for item in saved_facts],
            documents=documents,
            mode=request.mode
        )
    except Exception:
        if documents:
            response = _context_fallback(message, documents)
        else:
            response = (
                "I am KAYA, your local learning companion. I can already help with calculator math, "
                "grade-12 math patterns, saved memory, and uploaded books/data. For full open-ended "
                "AI replies, connect Ollama with the qwen2.5:3b model."
            )

    _persist_learning(message, response, session_id, request.mode, request.save_training, [])

    return ChatResponse(response=response, session_id=session_id, mode=request.mode)


def _context_fallback(
    message: str,
    documents: list[str]
) -> str:

    joined = "\n\n".join(documents[:2])
    return (
        "I found related local knowledge for your question. Ollama is not connected right now, "
        "so I cannot synthesize a full AI answer yet. Here is the best local context I found:\n\n"
        f"{joined}\n\nQuestion: {message}"
    )


def _persist_learning(
    message: str,
    response: str,
    session_id: str,
    mode: str,
    save_training: bool,
    extra_tags: list[str],
) -> None:

    remember_conversation(message, response, session_id)

    for fact in extract_new_knowledge(message, response):
        save_fact(
            fact,
            source=f"chat:{session_id}",
            created_at=datetime.now(timezone.utc).isoformat()
        )

    if save_training and response:
        add_training_example(
            message,
            response,
            tags=["chat", mode, *extra_tags],
            rating=5
        )
