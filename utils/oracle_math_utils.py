import re

def oracle_should_use_calculator(text: str) -> bool:
    """
    Ideal / future math capability (broader than agent).
    """
    text = text.lower()

    patterns = [
        r"\d+\s*[\+\-\*/]\s*\d+",                   # basic math
        r"\d+\s*[\+\-\*/]\s*\d+\s*[\+\-\*/]\s*\d+", # multi-op
        r"\([\d\+\-\*/\s\.]+\)",                    # parentheses
        r"add|plus|minus|times|divide|sum",         # natural language
    ]

    return any(re.search(p, text) for p in patterns)
