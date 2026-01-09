from langgraph.graph import StateGraph, START, END
from schemas.state import GraphState
from agents.test_writer import write_tests
from evaluation.evaluator import evaluate
from utils.file_utils import save_test_cases
from utils.langsmith_dataset import upload_test_cases
from langsmith import traceable

def build_graph():
    graph = StateGraph(GraphState)

    def write_node(state):
        return {"test_cases": write_tests(state["agent_spec"], state["tools"])}

    @traceable(run_type="tool", name="save_test_cases")
    def save_node(state):
        path = save_test_cases(state["test_cases"], state["agent_spec"]["name"])
        return {"test_cases_file": path}

    @traceable(run_type="tool", name="upload_dataset")
    def dataset_node(state):
        return upload_test_cases(
            f"{state['agent_spec']['name']}_dataset",
            state["test_cases"]
        )

    def evaluate_node(state):
        results, score = evaluate(state["test_cases"], state["tools"])
        return {"results": results, "final_score": score}

    graph.add_node("write_tests", write_node)
    graph.add_node("save_tests", save_node)
    graph.add_node("upload_dataset", dataset_node)
    graph.add_node("evaluate", evaluate_node)

    graph.add_edge(START, "write_tests")
    graph.add_edge("write_tests", "save_tests")
    graph.add_edge("save_tests", "upload_dataset")
    graph.add_edge("upload_dataset", "evaluate")
    graph.add_edge("evaluate", END)

    return graph.compile()
