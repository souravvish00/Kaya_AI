from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a KAYA supervised fine-tuning run from exported JSONL data."
    )
    parser.add_argument("--model", required=True, help="Base model name or local path.")
    parser.add_argument("--dataset", required=True, help="Path to training examples JSONL.")
    parser.add_argument("--method", default="lora", choices=["lora", "qlora", "full"])
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--learning-rate", type=float, default=0.0002)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the training plan without launching heavy training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset = Path(args.dataset)
    if not dataset.exists():
        raise SystemExit(f"Dataset not found: {dataset}")

    print("KAYA training plan")
    print(f"Base model: {args.model}")
    print(f"Dataset: {dataset}")
    print(f"Method: {args.method}")
    print(f"Epochs: {args.epochs}")
    print(f"Learning rate: {args.learning_rate}")
    print()
    print(
        "Heavy training is intentionally not launched by default. Install transformers, "
        "datasets, accelerate, peft, and torch in a GPU environment, then replace this "
        "dry runner with your actual SFT/LoRA trainer."
    )


if __name__ == "__main__":
    main()
