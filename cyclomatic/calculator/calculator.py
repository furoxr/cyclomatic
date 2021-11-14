import tree_sitter
from cyclomatic.calculator.base import Block
from cyclomatic.config import LANGUAGE_MAPPING
from typing import Optional


def calculate(node: tree_sitter.Node, language: str) -> Optional[Block]:
    """
    calculate the cyclomatic complexity from the ast root node
    """
    if node is None:
        return None

    calculator_cls = LANGUAGE_MAPPING[language][-1]
    calculator = calculator_cls()
    calculator.visit(node)
    return calculator.block
