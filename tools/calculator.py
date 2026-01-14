from langsmith import traceable
import ast
import operator as op

# Supported operators
_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Num):  # py<3.8
        return node.n
    if isinstance(node, ast.Constant):  # py3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPS:
            raise ValueError("Operator not allowed")
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPS:
            raise ValueError("Unary operator not allowed")
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))

    raise ValueError("Invalid expression")

@traceable(run_type="tool", name="calculator")
def calculator(expr: str):
    try:
        tree = ast.parse(expr, mode="eval")
        value = _safe_eval(tree.body)
        return str(value)
    except Exception:
        return "error"
