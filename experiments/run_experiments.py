from langsmith import Client
from agents.target_agent import TargetAgent
from tools.calculator import calculator

client = Client()

def runner(inputs: dict):
    agent = TargetAgent({"calculator": calculator})
    return agent.invoke(inputs["input"])

client.run_on_dataset(
    dataset_name="math_agent_dataset",
    llm_or_chain_factory=runner,
    experiment_name="math-agent-v1"
)
