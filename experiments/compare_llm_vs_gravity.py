from agents.test_writer import write_tests
from search.gravity_search import gravity_search
from search.normalize import normalize_gravity_tests
from tools.calculator import calculator
from agents.target_agent import TargetAgent

agent_spec = {
    "name": "math_agent",
    "purpose": "Solve math problems using tools"
}

tools = {"calculator": calculator}
agent = TargetAgent(tools)

llm_tests = write_tests(agent_spec, tools)
gravity_tests = normalize_gravity_tests(gravity_search(agent))

print("\n=== Ollama Test Cases ===")
for tc in llm_tests:
    print(tc["input"])

print("\n=== Gravity Search Test Cases ===")
for tc in gravity_tests:
    print(tc["input"])
