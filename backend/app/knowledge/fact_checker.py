from __future__ import annotations

import re


FACT_PATTERNS = [
    re.compile(r"\bmy name is\s+([A-Z][A-Za-z .'-]{1,60})", re.IGNORECASE),
    re.compile(r"\bi am\s+([A-Za-z][A-Za-z .'-]{2,80})", re.IGNORECASE),
    re.compile(r"\bi live in\s+([A-Za-z][A-Za-z .,'-]{2,80})", re.IGNORECASE),
    re.compile(r"\bi prefer\s+([A-Za-z0-9][A-Za-z0-9 .,'-]{2,100})", re.IGNORECASE),
    re.compile(r"\bremember that\s+(.{4,160})", re.IGNORECASE),
]


def extract_new_knowledge(
    user_message,
    assistant_response=None
):
    """Extract durable user facts worth saving as memory.

    This intentionally stays conservative so KAYA does not learn random chat text
    as a permanent fact.
    """
    del assistant_response

    facts = []
    text = " ".join(str(user_message).split())

    for pattern in FACT_PATTERNS:
        for match in pattern.finditer(text):
            fact = _normalize_fact(match.group(0))
            if fact and fact not in facts:
                facts.append(fact)

    return facts


def _normalize_fact(fact: str) -> str:
    fact = fact.strip(" .")
    if not fact:
        return ""
    return fact[0].upper() + fact[1:]
