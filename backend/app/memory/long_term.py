import json
from pathlib import Path
import uuid

MEMORY_FILE = Path(
    "data/memory/conversations.json"
)

FACTS_FILE = Path(
    "data/memory/facts.json"
)


def load_memory():

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if MEMORY_FILE.exists():

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return []


def save_memory(memory):

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=2
        )


def load_facts():

    FACTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if FACTS_FILE.exists():

        with open(
            FACTS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return []


def remember_conversation(
    user_message,
    assistant_message=None,
    session_id=None
):

    if session_id is None:
        session_id = str(uuid.uuid4())

    memory = load_memory()

    if assistant_message:

        memory.append({
            "session_id": session_id,
            "user": user_message,
            "assistant": assistant_message
        })

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory,
                f,
                indent=2
            )

    return session_id, memory[-10:]


def save_fact(
    fact,
    source="conversation",
    created_at=None
):

    FACTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if FACTS_FILE.exists():

        with open(
            FACTS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

    else:
        data = []

    if any(item.get("fact") == fact for item in data):
        return

    data.append({
        "fact": fact,
        "source": source,
        "created_at": created_at
    })

    with open(
        FACTS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )
