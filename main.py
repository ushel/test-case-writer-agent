import os
import logging
from graph.workflow import build_graph
from tools.calculator import calculator

os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
logging.getLogger("langsmith").setLevel(logging.ERROR)

if __name__ == "__main__":
    print("\n🚀 Starting Test-Case Writer Agent Pipeline")

    graph = build_graph()

    output = graph.invoke(
        {
            "agent_spec": {
                "name": "math_agent",
                "purpose": "Solve math problems",
                "constraints": ["Must use calculator"]
            },
            "tools": {
                "calculator": calculator
            }
        },
        config={
            "run_name": "test-case-writer-agent-run",
            "tags": ["agent-testing", "langgraph"]
        }
    )

    print("\n📁 Test cases saved at:")
    print(output["test_cases_file"])

    print("\n📊 LangSmith Dataset Info:")
    print("  Dataset name     :", output.get("dataset_name"))
    print("  Dataset uploaded :", output.get("dataset_uploaded"))

    print("\n🧪 Test Results:")
    for r in output["results"]:
        print(r)

    print("\n🎯 FINAL SCORE:", output["final_score"])
