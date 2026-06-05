from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

DOCUMENTS_FILE = Path("data/knowledge/documents.json")
CHUNKS_FILE = Path("data/knowledge/chunks.jsonl")


def ingest_document(
    title: str,
    text: str,
    source: str = "manual"
) -> dict:

    cleaned = _clean_text(text)
    if not cleaned:
        raise ValueError("No readable text found in this source.")

    document = {
        "id": str(uuid4()),
        "title": title.strip() or "Untitled source",
        "source": source,
        "characters": len(cleaned),
        "chunks": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    chunks = [
        {
            "id": str(uuid4()),
            "document_id": document["id"],
            "title": document["title"],
            "text": chunk,
            "source": source,
            "created_at": document["created_at"]
        }
        for chunk in _chunk_text(cleaned)
    ]
    document["chunks"] = len(chunks)

    documents = list_documents()
    documents.append(document)
    _write_json(DOCUMENTS_FILE, documents)
    _append_chunks(chunks)

    return document


def list_documents() -> list[dict]:

    if not DOCUMENTS_FILE.exists():
        return []

    with open(
        DOCUMENTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def list_chunks(
    limit: int = 100
) -> list[dict]:

    if not CHUNKS_FILE.exists():
        return []

    chunks = []

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks[-limit:]


def retrieve_context(
    query: str,
    limit: int = 4
) -> list[str]:

    words = {
        word
        for word in re.findall(r"[a-z0-9]+", query.lower())
        if len(word) > 2
    }
    if not words:
        return []

    scored = []
    for chunk in list_chunks(limit=1000):
        haystack = chunk["text"].lower()
        score = sum(1 for word in words if word in haystack)
        if score:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        f"Source: {chunk['title']}\n{chunk['text']}"
        for _, chunk in scored[:limit]
    ]


def _clean_text(text: str) -> str:

    return re.sub(r"\s+", " ", text).strip()


def _chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 160
) -> list[str]:

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(end - overlap, start + 1)

    return chunks


def _write_json(
    path: Path,
    data: list[dict]
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def _append_chunks(
    chunks: list[dict]
) -> None:

    CHUNKS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CHUNKS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        for chunk in chunks:
            f.write(json.dumps(chunk) + "\n")
