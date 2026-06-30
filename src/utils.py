import json


def load_jsonl(path):
    """
    Reads large JSONL file line by line.
    This avoids loading the full 400MB+ file into memory.
    """
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                yield json.loads(line)


def safe_get(data, keys, default=""):
    """
    Safely access nested dictionary values.
    Example:
    safe_get(candidate, ["profile", "headline"])
    """
    current = data

    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default

    return current if current is not None else default


def normalize_text(value):
    """
    Converts any text/list/dict value into lowercase searchable text.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value.lower()

    if isinstance(value, list):
        return " ".join(normalize_text(item) for item in value)

    if isinstance(value, dict):
        return " ".join(normalize_text(v) for v in value.values())

    return str(value).lower()