from typing import TypedDict, List, Dict, Any, Optional

class TestCase(TypedDict):
    id: str
    input: Any
    expected_tool: Optional[str]
    expected_behavior: str

class TestResult(TypedDict):
    test_id: str
    tool_called: Optional[str]
    score: float

class GraphState(TypedDict):
    agent_spec: Dict[str, Any]
    tools: Dict[str, Any]

    test_cases: List[TestCase]
    test_cases_file: str

    dataset_name: str
    dataset_uploaded: bool

    results: List[TestResult]
    final_score: float
