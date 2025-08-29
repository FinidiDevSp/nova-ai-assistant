"""Plugin to evaluate arithmetic expressions safely."""
from __future__ import annotations

import ast
import operator
import re

from . import BasePlugin


class Plugin(BasePlugin):
    """Evaluate simple arithmetic expressions using AST for safety."""

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        ops = ["más", "mas", "menos", "por", "entre"]
        return any(op in text for op in ops) and bool(re.search(r"\d", text))

    def handle(self, text: str) -> str:
        text = text.lower()
        replacements = {
            "más": "+",
            "mas": "+",
            "menos": "-",
            "por": "*",
            "entre": "/",
        }
        for word, symbol in replacements.items():
            text = text.replace(word, symbol)
        expr = "".join(ch for ch in text if ch in "0123456789+-*/.()")
        if not expr:
            return "No se encontró una expresión válida"
        try:
            result = self._safe_eval(expr)
        except Exception:
            return "Error al evaluar la expresión"
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)

    def _safe_eval(self, expression: str) -> float:
        node = ast.parse(expression, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
            }
            op_type = type(node.op)
            if op_type in operators:
                return operators[op_type](left, right)
            raise ValueError("Operador no permitido")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._eval_node(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Num):  # pragma: no cover
            return node.n
        raise ValueError("Expresión no permitida")
