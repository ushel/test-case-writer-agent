import json
import re

def extract_json(text: str):
    if not text or not text.strip():
        raise ValueError("Empty LLM output")

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found")
