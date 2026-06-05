from __future__ import annotations

import ast
import math
import statistics
from decimal import Decimal, getcontext

getcontext().prec = 40

ALLOWED_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "factorial": math.factorial,
    "floor": math.floor,
    "ceil": math.ceil,
    "gcd": math.gcd,
    "lcm": math.lcm,
    "mean": statistics.mean,
    "median": statistics.median,
    "stdev": statistics.stdev,
    "Decimal": Decimal,
    "pi": math.pi,
    "e": math.e,
}

ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
)


def calculate(expression: str) -> dict:
    cleaned = _clean_expression(expression)
    if not cleaned:
        return {"ok": False, "error": "No expression provided."}

    try:
        tree = ast.parse(cleaned, mode="eval")
        _validate_tree(tree)
        result = eval(compile(tree, "<calculator>", "eval"), {"__builtins__": {}}, ALLOWED_NAMES)
    except Exception as error:
        return {"ok": False, "expression": cleaned, "error": str(error)}

    return {
        "ok": True,
        "expression": cleaned,
        "result": _format_result(result),
    }


def looks_like_calculation(message: str) -> bool:
    lowered = message.lower().strip()
    triggers = ("calculate", "calc", "solve", "math", "=")
    math_symbols = ("+", "-", "*", "/", "^", "sqrt", "sin", "cos", "tan", "log")
    expression_only = any(char.isdigit() for char in lowered) and any(
        symbol in lowered for symbol in math_symbols
    )
    return expression_only or (
        any(trigger in lowered for trigger in triggers)
        and any(symbol in lowered for symbol in math_symbols)
    )


def _clean_expression(expression: str) -> str:
    cleaned = expression.strip()
    for prefix in ("calculate", "calc", "solve", "math"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip(" :")
    return cleaned.replace("^", "**")


def _validate_tree(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in ALLOWED_NAMES:
            raise ValueError(f"Unknown name: {node.id}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_NAMES:
                raise ValueError("Only approved calculator functions can be called.")


def _format_result(result: object) -> str:
    if isinstance(result, float):
        return f"{result:.12g}"
    return str(result)
