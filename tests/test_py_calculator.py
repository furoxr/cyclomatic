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

    # module cyclomatic complexity
    assert c.block.score == 3

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 2


def test_for():
    code = """
def fun(a):
    for i in range(100):
        a += i
    return a
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    # module cyclomatic complexity
    assert c.block.score == 3

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 2


def test_compose():
    code = """
def fun(a):
    for i in range(100):
        a += i
    if a > 200:
        a -= 40
    else:
        a = a * a
    while a > 150:
        a -= 1
    return a
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    print(c.block)
    # module cyclomatic complexity
    assert c.block.score == 6

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 5


def test_nested():
    code = """
def fun(a):
    for i in range(100):
        if i > 50:
            a += 2
        else:
            a += 3
        a += i
    return a
"""
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    # module cyclomatic complexity
    assert c.block.score == 5

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 4


def test_nested_function():
    code = """
def fun(a):
    def wrap():
        if a > 0:
            return 1
        else:
            return 0
 
    for i in range(100):
        if i > 50:
            a += 2
        else:
            a += 3
        a += i
    return a + wrap()
    """
    tree, _ = to_ast(source=code.encode('utf-8'), language='py')
    c = PyCalculator()
    c.visit(tree.root_node)

    print(c.block)
    # module cyclomatic complexity
    assert c.block.score == 8

    # function cyclomatic complexity
    assert c.block.sub_blocks[0].score == 7

    # nest function cyclomatic complexity
    assert c.block.sub_blocks[0].sub_blocks[0].score == 3
