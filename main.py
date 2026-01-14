import os
import logging
from graph.workflow import build_graph
from tools.calculator import calculator

# --------------------------------------------------
# LangSmith (best-effort, never crash)
# --------------------------------------------------
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault("LANGSMITH_PROJECT", "test-case-writer-agent")
logging.getLogger("langsmith").setLevel(logging.ERROR)

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    print("\nStarting Test-Case Writer Agent Pipeline")

    # Build LangGraph
    graph = build_graph()

    # Invoke graph
    output = graph.invoke(
        {
            "agent_spec": {
                "name": "math_agent",
                "purpose": "Solve math problems using tools",
                "constraints": ["Must use calculator"]
            },
            "tools": {
                "calculator": calculator
            }
        },
        config={
            "run_name": "test-case-writer-agent-run",
            "tags": [
                "agent-testing",
                "tool-eval",
                "langgraph",
                "ollama"
            ],
        }
    )

    # --------------------------------------------------
    # PRINT ARTIFACT LOCATIONS
    # --------------------------------------------------
    print("\nArtifacts generated:")
    print("  Test cases (expected):")
    print("     ", output.get("test_cases_file", "N/A"))

    print("  Test results (actual):")
    print("     ", output.get("results_file", "N/A"))

    print("  Evaluation summary:")
    print("     ", output.get("evaluation_file", "N/A"))

    # --------------------------------------------------
    # DATASET STATUS (LangSmith)
    # --------------------------------------------------
    print("\nLangSmith Dataset Info:")
    print("  Dataset name     :", output.get("dataset_name", "N/A"))
    print("  Dataset uploaded :", output.get("dataset_uploaded", False))

    # --------------------------------------------------
    # PRINT DETAILED RESULTS
    # --------------------------------------------------
    print("\nDetailed Test Results:")
    for r in output.get("results", []):
        print(
            f"  {r['test_id']} | "
            f"expected={r.get('expected_tool')} | "
            f"actual={r.get('actual_tool')} | "
            f"score={r['score']}"
        )

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------
    print("\nFINAL SCORE:", output.get("final_score", 0.0))
