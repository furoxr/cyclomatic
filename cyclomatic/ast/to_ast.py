import pathlib
from tree_sitter import (Language, Parser, Tree)
from cyclomatic.config import package_path, LANGUAGE_MAPPING
from typing import Tuple


SO_PATH = str(package_path / 'ast' / 'tree_sitter_binding.so')
Language.build_library(SO_PATH, [str(s[0]) for s in LANGUAGE_MAPPING.values()])


def to_ast(*, source: bytes = None, path: str = None, language=None) -> Tuple[Tree, str]:
    """
    convert source file or souce to a tree_sitter.Tree

    :param source: souce code
    :param path: source file path
    :param language: supported language in
    :return: tree_sitter.Tree
    """
    if path:
        if language is None:
            path = pathlib.Path(path)
            suffix = path.suffix[1:]
            language = suffix

        if language not in LANGUAGE_MAPPING:
            raise NotImplementedError(path.suffix[1:])

        with open(path, 'rb') as f:
            source = f.read()
    elif source and language:
        pass
    else:
        raise Exception(
            "Wrong parameters! Try:\n"
            "to_ast(path='path/to/source')\n"
            "to_ast(path='path/to/source', language='py')\n"
            "to_ast(source=b'def fun():\n    return 0')\n"
        )

    tree_sitter_lang = Language(SO_PATH, LANGUAGE_MAPPING[language][1])
    parser = Parser()
    parser.set_language(tree_sitter_lang)
    return parser.parse(source), language
