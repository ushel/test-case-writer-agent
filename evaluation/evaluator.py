from agents.target_agent import TargetAgent

def evaluate(test_cases: list, tools: dict):
    agent = TargetAgent(tools)

    results = []
    detailed_results = []

    for tc in test_cases:
        actual = agent.invoke(tc.get("input"))

        tool_calls = actual.get("tool_calls", [])
        tool_called = tool_calls[0]["tool"] if tool_calls else None
        expected_tool = tc.get("expected_tool")

        if expected_tool is None:
            score = 1.0 if tool_called is None else 0.0
        else:
            score = 1.0 if tool_called == expected_tool else 0.0

        result = {
            "test_id": tc.get("id"),
            "input": tc.get("input"),
            "expected_tool": expected_tool,
            "actual_tool": tool_called,
            "actual_output": actual.get("final_answer"),
            "score": score
        }

        detailed_results.append(result)

        results.append({
            "test_id": tc.get("id"),
            "tool_called": tool_called,
            "score": score
        })

    final_score = round(
        sum(r["score"] for r in results) / max(len(results), 1),
        2
    )

    return detailed_results, final_score
