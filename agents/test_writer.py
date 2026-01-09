import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from utils.json_utils import extract_json

MIN_TESTS = 7
RETRIES = 3

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a Test-Writer Agent.

Rules:
- Generate AT LEAST 7 test cases
- Each test MUST include:
  - id
  - input
  - expected_tool (null if none)
  - expected_behavior
- Output VALID JSON ONLY
"""),
    ("user", """
Agent spec:
{agent_spec}

Available tools:
{tools}

Return JSON ARRAY of COMPLETE test cases.
""")
])

def normalize_test_cases(test_cases: list) -> list:
    normalized = []

    for i, tc in enumerate(test_cases, start=1):
        tc = dict(tc)

        tc.setdefault("id", f"TC-{i}")
        tc.setdefault("input", "")
        tc.setdefault("expected_tool", None)
        tc.setdefault("expected_behavior", "Should behave correctly")

        normalized.append(tc)

    return normalized

def write_tests(agent_spec: dict, tools: dict):
    llm = ChatOllama(model="llama3.1:8b", temperature=0)

    for _ in range(RETRIES):
        messages = PROMPT.format_messages(
            agent_spec=json.dumps(agent_spec, indent=2),
            tools=list(tools.keys())
        )

        raw = llm.invoke(messages).content
        tests = extract_json(raw)

        if isinstance(tests, list) and len(tests) >= MIN_TESTS:
            return normalize_test_cases(tests)

    raise RuntimeError("Failed to generate minimum test cases")
