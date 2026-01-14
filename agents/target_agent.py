from langsmith import traceable
from typing import Any
from utils.math_utils import should_use_calculator, extract_expression



from utils.math_utils import (
    should_use_calculator,
    extract_expression,
)


class TargetAgent:
    def __init__(self, tools: dict):
        self.tools = tools

    # --------------------------------------------------
    # Normalize input
    # --------------------------------------------------
    def _normalize_input(self, user_input: Any) -> str:
        if isinstance(user_input, str):
            return user_input

        if isinstance(user_input, dict):
            for k in ("input", "question", "query", "text", "problem"):
                if k in user_input and isinstance(user_input[k], str):
                    return user_input[k]
            return str(user_input)

        return str(user_input)

    # --------------------------------------------------
    # Agent entrypoint
    # --------------------------------------------------
    @traceable(run_type="chain", name="target_agent_invoke")
    def invoke(self, user_input):
        text = self._normalize_input(user_input).lower().strip()
        tool_calls = []

        # --------------------------------------------------
        # SINGLE SOURCE OF TRUTH FOR TOOL USAGE
        # --------------------------------------------------
        if should_use_calculator(text):

            if "calculator" not in self.tools:
                return {
                    "final_answer": "Calculator unavailable",
                    "tool_calls": []
                }

            expr = extract_expression(text)

            result = self.tools["calculator"](expr)

            tool_calls.append({
                "tool": "calculator",
                "input": expr,
                "output": result
            })

            return {
                "final_answer": result,
                "tool_calls": tool_calls
            }

        # --------------------------------------------------
        # NON-MATH FALLBACK
        # --------------------------------------------------
        return {
            "final_answer": "I don't know",
            "tool_calls": []
        }
