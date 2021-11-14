import tree_sitter
import dataclasses
import typing


class TreeSitterNodeVisitor:
    def visit(self, node: tree_sitter.Node):
        method = 'visit_' + node.type
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: tree_sitter.Node):
        for _node in node.children:
            if _node.is_named:
                self.visit(_node)


@dataclasses.dataclass
class Block:
    id: int
    name_pos: typing.Tuple[int, int]
    score: float = 0
    sub_blocks: typing.List['Block'] = dataclasses.field(default_factory=list)
