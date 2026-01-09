import json
from pathlib import Path
from datetime import datetime

def save_test_cases(test_cases: list, agent_name: str) -> str:
    """
    Save generated test cases to disk.
    Returns the file path.
    """
    base_dir = Path("artifacts/test_cases")
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = base_dir / f"{agent_name}_tests_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(test_cases, f, indent=2)

    return str(file_path)
