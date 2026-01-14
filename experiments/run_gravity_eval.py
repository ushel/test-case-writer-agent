from agents.target_agent import TargetAgent
from tools.calculator import calculator
from search.gravity_search import gravity_search
from evaluation.evaluator import evaluate
from utils.file_utils import save_test_cases

if __name__ == "__main__":
    print("\nRunning Gravity Search for Test Case Generation...")

    agent = TargetAgent({"calculator": calculator})

    # ----------------------------------
    # 1. Generate Gravity test cases
    # ----------------------------------
    gravity_tests = gravity_search(agent)

    print(f"Generated {len(gravity_tests)} Gravity-based test cases")

    print("\nGravity Test Cases:")
    for tc in gravity_tests:
        print(
            f"{tc['input']} | expected={tc['expected_tool']}"
        )

    # ----------------------------------
    # 2. SAVE Gravity test cases (KEY FIX)
    # ----------------------------------
    path = save_test_cases(
        gravity_tests,
        agent_name="math_agent_gravity"
    )

    print("\nGravity test cases saved at:")
    print("   ", path)

    # ----------------------------------
    # 3. Evaluate using saved test cases
    # ----------------------------------
    print("\nEvaluating agent using Gravity-based test cases...")

    detailed_results, final_score = evaluate(
        gravity_tests,
        {"calculator": calculator}
    )

    for r in detailed_results:
        print(
            f"{r['test_id']} | "
            f"expected={r['expected_tool']} | "
            f"actual={r['actual_tool']} | "
            f"score={r['score']}"
        )

    print("\nFINAL GRAVITY SCORE:", final_score)
