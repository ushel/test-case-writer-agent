from langsmith import traceable

@traceable(run_type="tool", name="calculator")
def calculator(expr: str):
    try:
        return str(eval(expr))
    except Exception:
        return "error"
