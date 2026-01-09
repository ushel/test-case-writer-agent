from langsmith import traceable
from agents.target_agent import TargetAgent

@traceable(run_type="tool", name="evaluate_target_agent")
def evaluate(test_cases: list, tools: dict):
    agent = TargetAgent(tools)
    results = []

    for tc in test_cases:
        out = agent.invoke(tc.get("input"))
        tool_calls = out.get("tool_calls", [])
        tool_called = tool_calls[0]["tool"] if tool_calls else None
        expected_tool = tc.get("expected_tool")

        if expected_tool is None:
            score = 1.0 if tool_called is None else 0.0
        else:
            score = 1.0 if tool_called == expected_tool else 0.0

        results.append({
            "test_id": tc.get("id"),
            "tool_called": tool_called,
            "score": score
        })

    final_score = sum(r["score"] for r in results) / max(len(results), 1)
    return results, round(final_score, 2)
