import os
import logging
from graph.workflow import build_graph
from tools.calculator import calculator
from graph.workflow import build_graph


# --------------------------------------------------
# LangSmith (best-effort, never crash)
# --------------------------------------------------
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
logging.getLogger("langsmith").setLevel(logging.ERROR)

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 Starting Test-Case Writer Agent Pipeline")

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
    print("     ", output.get("test_cases_file"))

    print("  Test results (actual):")
    print("     ", output.get("results_file"))

    print("  Evaluation summary:")
    print("     ", output.get("evaluation_file"))

    # --------------------------------------------------
    # DATASET STATUS (LangSmith)
    # --------------------------------------------------
    print("\nLangSmith Dataset Info:")
    print("  Dataset name     :", output.get("dataset_name"))
    print("  Dataset uploaded :", output.get("dataset_uploaded", False))

    # --------------------------------------------------
    # PRINT DETAILED RESULTS
    # --------------------------------------------------
    print("\nDetailed Test Results:")
    for r in output["results"]:
        print(
            f"  {r['test_id']} | "
            f"expected={r['expected_tool']} | "
            f"actual={r['actual_tool']} | "
            f"score={r['score']}"
        )

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------
    print("\nFINAL SCORE:", output["final_score"])
