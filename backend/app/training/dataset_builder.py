import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

DATASET_FILE = Path(
    "data/datasets/train/chat_train.jsonl"
)
EXPORT_FILE = Path(
    "data/datasets/train/openai_chat_train.jsonl"
)
JOBS_FILE = Path(
    "data/datasets/train/jobs.json"
)


def add_training_example(
    prompt,
    completion,
    tags=None,
    rating=5
):

    DATASET_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "id": str(uuid4()),
        "prompt": prompt,
        "response": completion,
        "completion": completion,
        "tags": tags or [],
        "rating": rating,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    with open(
        DATASET_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(record)
            + "\n"
        )

    return record


def list_training_examples():

    if not DATASET_FILE.exists():
        return []

    examples = []

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    return examples


def dataset_stats():

    examples = list_training_examples()
    high_quality = sum(1 for example in examples if example.get("rating", 0) >= 4)

    return {
        "examples": len(examples),
        "high_quality": high_quality,
        "ready_for_finetune": high_quality >= 20,
        "dataset_file": str(DATASET_FILE),
        "export_file": str(EXPORT_FILE)
    }


def export_openai_jsonl():

    examples = list_training_examples()
    EXPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        EXPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        for example in examples:
            record = {
                "messages": [
                    {"role": "user", "content": example["prompt"]},
                    {"role": "assistant", "content": example.get("response") or example["completion"]}
                ]
            }
            f.write(json.dumps(record) + "\n")

    return {
        "examples": len(examples),
        "path": str(EXPORT_FILE)
    }


def list_training_jobs():

    if not JOBS_FILE.exists():
        return []

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def create_training_job(
    model_name,
    method,
    epochs,
    learning_rate
):

    JOBS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    jobs = list_training_jobs()
    job = {
        "id": str(uuid4()),
        "model_name": model_name,
        "method": method,
        "epochs": epochs,
        "learning_rate": learning_rate,
        "command": (
            "python scripts/train_model.py "
            f"--dataset {EXPORT_FILE} --model {model_name} --method {method} "
            f"--epochs {epochs} --learning-rate {learning_rate}"
        ),
        "status": "configured"
    }
    jobs.append(job)

    with open(
        JOBS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            jobs,
            f,
            indent=2
        )

    return job
