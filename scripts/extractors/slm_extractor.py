import json
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("🔄 Loading SLM model...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="cpu",
            dtype=torch.float32
        )

    return _tokenizer, _model


def _safe_json_from_text(text):
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    obj = re.search(r"\{.*\}", text, re.DOTALL)
    if obj:
        try:
            return json.loads(obj.group())
        except json.JSONDecodeError:
            pass

    arr = re.search(r"\[.*\]", text, re.DOTALL)
    if arr:
        try:
            return json.loads(arr.group())
        except json.JSONDecodeError:
            pass

    return None


def extract_with_slm(text, doc_type):
    tokenizer, model = load_model()

    prompt = f"""
You are an information extraction system.

Document type: {doc_type}

Return ONLY valid JSON.

Electricity Bill:
{{ meter_id, bill_date, kwh, amount_payable, location }}

Math Book:
[ {{ unit, section, example_number, example_title }} ]

Constitution:
[
  {{
    article_number,
    article_title,
    part,
    part_title,
    article_text
  }}
]

Text:
{text[:3000]}
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs,max_new_tokens=256,do_sample=False)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    parsed = _safe_json_from_text(response)

    if parsed is None:
        return [] if doc_type in ["Constitution", "Math Book"] else {}

    if doc_type in ["Constitution", "Math Book"]:
        return parsed if isinstance(parsed, list) else [parsed]

    return parsed if isinstance(parsed, dict) else {}