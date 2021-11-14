import logging
import tree_sitter
import typing

from cyclomatic.calculator.base import TreeSitterNodeVisitor, Block


_logger = logging.getLogger(__name__)


class PyCalculator(TreeSitterNodeVisitor):
    """calculate the cyclomatic complexity. cyclomatic complexity = num of decesion points + 1"""

    language_tag = 'py'

    # decesion point pattern
    decesion_stmts = (
        'if_statement',
        'elif_clause',
        'else_clause',
        'while_statement',
        'for_statement',
        'except_clause'
    )

    def __init__(self):
        self.id = 1
        self.block_stack: typing.List[Block] = []
        self.block = None

    @property
    def current_block(self):
        """current block is the current context when calculating the cyclomatic complexity"""
        if self.block_stack:
            return self.block_stack[-1]
        return None

    def generic_visit(self, node: tree_sitter.Node):
        if node.type in self.decesion_stmts:
            # if decesion statment found, add one to the current_block.score
            self.current_block.score += 1

        for _node in node.children:
            if _node.is_named:
                self.visit(_node)

    def visit_module(self, node: tree_sitter.Node):
        block = Block(self.id, (0, 0))
        self.id += 1
        self.block_stack.append(block)
        self.generic_visit(node)
        self.block_stack.pop()
        sub_score = sum([b.score for b in block.sub_blocks])
        # when the traverse completes, block.score is the num of decesion point
        block.score += sub_score + 1
        self.block = block

    def visit_class_definition(self, node: tree_sitter.Node):
        name_node = node.child_by_field_name('name')
        block = Block(id=self.id, name_pos=(name_node.start_byte, name_node.end_byte))
        self.id += 1
        if self.current_block:
            self.current_block.sub_blocks.append(block)
        self.block_stack.append(block)
        self.generic_visit(node)
        self.block_stack.pop()
        sub_score = sum([b.score for b in block.sub_blocks])

        # when the traverse completes, block.score is the num of decesion point
        block.score += sub_score + 1

    def visit_function_definition(self, node: tree_sitter.Node):
        name_node = node.child_by_field_name('name')
        block = Block(id=self.id, name_pos=(name_node.start_byte, name_node.end_byte))
        self.id += 1
        if self.current_block:
            self.current_block.sub_blocks.append(block)
        self.block_stack.append(block)
        self.generic_visit(node)
        self.block_stack.pop()
        # when the traverse completes, block.score is the num of decesion point
        sub_score = sum([b.score for b in block.sub_blocks])
        block.score += sub_score + 1
