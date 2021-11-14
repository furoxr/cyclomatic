import tree_sitter
from cyclomatic.calculator.base import Block
from cyclomatic.config import LANGUAGE_MAPPING


def calculate(node: tree_sitter.Node, language: str) -> Block:
    """
    calculate the cyclomatic complexity from the ast root node
    """
    calculator_cls = LANGUAGE_MAPPING[language][-1]
    calculator = calculator_cls()
    calculator.visit(node)
    return calculator.block
