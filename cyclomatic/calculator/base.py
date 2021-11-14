import tree_sitter
import warnings
import dataclasses
import typing
from cyclomatic.config import LANGUAGE_MAPPING


class TreeSitterNodeVisitor:

    language_tag = None

    def __init_subclass__(cls, **kwargs):
        # auto register calculator into the language mapping,
        # so the top level api cloud auto use the corrosponding calculator
        if cls.language_tag is None:
            raise Exception(f'calculator:{cls} does not have the language_tag property.')
        if cls.language_tag not in LANGUAGE_MAPPING:
            warnings.warn(
                f'language_tag:{cls.language_tag} does not have the corresponding tree-sitter parser',
                Warning
            )
            return

        LANGUAGE_MAPPING[cls.language_tag][-1] = cls

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
