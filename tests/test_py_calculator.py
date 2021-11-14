import pytest
from cyclomatic.calculator.py_calculator import PyCalculator
from cyclomatic.ast.to_ast import to_ast


def test_simple_if():
    code = """\
def fun(a):
    if a:
        return a
    return 0
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    # module cyclomatic complexity
    assert c.block.score == 3

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 2


def test_simple_while():
    code = """
def fun(a):
    while a > 100:
        a -= 1
    return a
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    # module cyclomatic complexity
    assert c.block.score == 3

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 2


def test_try_catch():
    code = """
def fun(a):
    a = a - a
    try:
        b = 100 / a
    except Exception:
        b = None
    return b
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    print(c.block)
    # module cyclomatic complexity
    assert c.block.score == 3

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 2

