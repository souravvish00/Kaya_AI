from fastapi import APIRouter

from ..memory.long_term import load_facts, load_memory, save_memory

router = APIRouter()


@router.get("/memory")
def get_memory():
    return {
        "memory": load_memory(),
        "facts": load_facts()
    }


@router.put("/memory")
def update_memory(memory: dict):
    save_memory(memory)
    return {"memory": memory}
