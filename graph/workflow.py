from langgraph.graph import StateGraph, START, END

from agents.test_writer import write_tests
from evaluation.evaluator import evaluate
from utils.file_utils import (
    save_test_cases,
    save_test_results,
    save_evaluation_summary,
)
from utils.langsmith_dataset import upload_test_cases


def build_graph():
    """
    Builds and returns the LangGraph pipeline.
    """

    graph = StateGraph(dict)

    # --------------------------------------------------
    # 1. Generate test cases
    # --------------------------------------------------
    def write_node(state):
        test_cases = write_tests(
            state["agent_spec"],
            state["tools"]
        )
        return {
            "agent_spec": state["agent_spec"],
            "tools": state["tools"],
            "test_cases": test_cases,
        }

    # --------------------------------------------------
    # 2. Save test cases (EXPECTED)
    # --------------------------------------------------
    def save_tests_node(state):
        agent_name = state["agent_spec"]["name"]
        path = save_test_cases(state["test_cases"], agent_name)

        return {
            "agent_spec": state["agent_spec"],
            "tools": state["tools"],
            "test_cases": state["test_cases"],
            "test_cases_file": path,
        }

    # --------------------------------------------------
    # 3. Upload dataset to LangSmith (BEST-EFFORT)
    # --------------------------------------------------
    def dataset_node(state):
        agent_name = state["agent_spec"]["name"]

        dataset_result = upload_test_cases(
            f"{agent_name}_dataset",
            state["test_cases"]
        )

        return {
            **state,
            **dataset_result,
        }

    # --------------------------------------------------
    # 4. Evaluate agent + save ACTUAL results
    # --------------------------------------------------
    def evaluate_node(state):
        agent_name = state["agent_spec"]["name"]

        detailed_results, final_score = evaluate(
            state["test_cases"],
            state["tools"]
        )

        results_file = save_test_results(
            detailed_results,
            agent_name
        )

        evaluation_file = save_evaluation_summary(
            {
                "final_score": final_score,
                "num_tests": len(detailed_results),
            },
            agent_name
        )

        return {
            **state,
            "results": detailed_results,
            "final_score": final_score,
            "results_file": results_file,
            "evaluation_file": evaluation_file,
        }

    # --------------------------------------------------
    # Graph wiring
    # --------------------------------------------------
    graph.add_node("write_tests", write_node)
    graph.add_node("save_tests", save_tests_node)
    graph.add_node("upload_dataset", dataset_node)
    graph.add_node("evaluate", evaluate_node)

    graph.add_edge(START, "write_tests")
    graph.add_edge("write_tests", "save_tests")
    graph.add_edge("save_tests", "upload_dataset")
    graph.add_edge("upload_dataset", "evaluate")
    graph.add_edge("evaluate", END)

    return graph.compile()
