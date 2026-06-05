from fastapi import APIRouter

from ..database.schemas import TrainingExample, TrainingJobRequest
from ..training.math_grade_12 import GRADE_12_MATH_EXAMPLES
from ..training.dataset_builder import (
    add_training_example,
    create_training_job,
    dataset_stats,
    export_openai_jsonl,
    list_training_examples,
    list_training_jobs,
)

router = APIRouter()


@router.get("/training/status")
def training_status():
    return {"stats": dataset_stats(), "jobs": list_training_jobs()}


@router.get("/training/examples")
def training_examples():
    return {"examples": list_training_examples()}


@router.post("/training/examples")
def create_training_example(example: TrainingExample):
    return {"example": add_training_example(**example.model_dump())}


@router.post("/training/export")
def export_training_dataset():
    return export_openai_jsonl()


@router.post("/training/jobs")
def configure_training_job(job: TrainingJobRequest):
    return {"job": create_training_job(**job.model_dump())}


@router.post("/training/seed/math-grade-12")
def seed_grade_12_math():
    examples = [
        add_training_example(**example)
        for example in GRADE_12_MATH_EXAMPLES
    ]
    return {"examples": len(examples), "tags": ["math", "grade-12"]}
