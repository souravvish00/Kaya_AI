MODEL_NAME = "Qwen/Qwen3-8B"


def load_model():
    """Load the configured model lazily so importing the API stays fast."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return tokenizer, model
