import random
from typing import Dict, List
from agents.target_agent import TargetAgent
from utils.oracle_math_utils import oracle_should_use_calculator

CANDIDATES = [
    "calculate 2 + 2",
    "calculate 10 / 5",
    "calculate apple",
    "calculate",
    "2 + two",
    "two + 2",
    "what is 2+2",
    "2 ** 3",
    "hello",
    "random text",
    "5 * 3",
    "divide 4 by 2",
    "add 2 and 3",
    "sum of 4 and 5",
    "(2 + 3) * 4",
]

def generate_test() -> Dict:
    text = random.choice(CANDIDATES)

    expected_tool = (
        "calculator"
        if oracle_should_use_calculator(text)
        else None
    )

    return {
        "input": text,
        "expected_tool": expected_tool,
        "expected_behavior": (
            "Should use calculator"
            if expected_tool
            else "Should NOT use calculator"
        )
    }

def gravity_search(
    agent: TargetAgent,
    population_size: int = 40,
    iterations: int = 1,
) -> List[Dict]:
    """
    Oracle-based Gravity Search:
    Expected behavior comes from the oracle, not the agent.
    """
    return [generate_test() for _ in range(population_size)]
