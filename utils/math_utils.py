import re

WORD_OPS = {
    "plus": "+",
    "add": "+",
    "sum": "+",
    "minus": "-",
    "subtract": "-",
    "times": "*",
    "multiply": "*",
    "multiplied": "*",
    "divide": "/",
    "divided": "/",
    "over": "/",
}

def normalize_words(text: str) -> str:
    t = text.lower()
    # Replace common word operators with symbols
    for w, sym in WORD_OPS.items():
        t = re.sub(rf"\b{w}\b", sym, t)
    # Convert "and" to space (helps "add 2 and 3")
    t = re.sub(r"\band\b", " ", t)
    return t

def extract_expression(text: str) -> str:
    """
    Extract a permissive math expression:
    keeps digits, operators, dots, parentheses, and spaces.
    """
    text = normalize_words(text)
    return re.sub(r"[^0-9\+\-\*/\.\(\)\s]", "", text).strip()

def is_valid_expression(expr: str) -> bool:
    """
    Allow:
    - multi-op: 2+3+4
    - parentheses: (2+3)*4
    - unary minus: -2+3
    - spaces
    Disallow:
    - empty / only operators
    - trailing operator
    """
    if not expr or not re.search(r"\d", expr):
        return False

    # No double operators like "++", "**", "//"
    if re.search(r"[\+\-\*/]{2,}", expr.replace("--", "+")):
        return False

    # Must not end with operator
    if re.search(r"[\+\-\*/]\s*$", expr):
        return False

    # Must contain at least one operator
    if not re.search(r"[\+\-\*/]", expr):
        return False

    # Parentheses basic balance check
    if expr.count("(") != expr.count(")"):
        return False

    return True

def should_use_calculator(text: str) -> bool:
    text = text.lower().strip()
    expr = extract_expression(text)
    return is_valid_expression(expr)
