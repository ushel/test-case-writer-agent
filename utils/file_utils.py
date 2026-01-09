import json
from pathlib import Path
from datetime import datetime

def _timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def save_test_cases(test_cases: list, agent_name: str) -> str:
    base = Path("artifacts/test_cases")
    base.mkdir(parents=True, exist_ok=True)

    path = base / f"{agent_name}_tests_{_timestamp()}.json"
    with open(path, "w") as f:
        json.dump(test_cases, f, indent=2)

    return str(path)


def save_test_results(results: list, agent_name: str) -> str:
    base = Path("artifacts/test_results")
    base.mkdir(parents=True, exist_ok=True)

    path = base / f"{agent_name}_results_{_timestamp()}.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2)

    return str(path)


def save_evaluation_summary(summary: dict, agent_name: str) -> str:
    base = Path("artifacts/evaluation")
    base.mkdir(parents=True, exist_ok=True)

    path = base / f"{agent_name}_eval_{_timestamp()}.json"
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

    return str(path)
