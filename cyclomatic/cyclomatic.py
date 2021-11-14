from typing import (
    Union,
    Optional,
    Dict
)
import logging
import pathlib
from cyclomatic.calculator.base import Block
from cyclomatic.ast.to_ast import to_ast
from cyclomatic.calculator import calculate


_logger = logging.getLogger(__name__)


def cyclomatic_singly(target: Union[str, bytes], language=None) -> Optional[Block]:
    """get cyclomatic complexity of the target.

    The target could be a file path str, or bytes of source code.
    This function will speculate the language according to the file suffix, but if source code provieded,
    language type should be explicitly given.
    """
    match target:
        case str(path):
            path_o = pathlib.Path(path)
            if path_o.is_file():
                tree, language = to_ast(path=path, language=language)
                if tree:
                    block = calculate(tree.root_node, language=language)
                    return block
            else:
                raise FileNotFoundError(path)
        case bytes(source):
            tree, language = to_ast(source=source, language=language)
            return calculate(tree.root_node, language=language)


def cyclomatic_in_batch(dir_path: str, language=None, ignore=True) -> Dict[str, Block]:
    """get the cyclomatic complexity list of the source files in the directory

    :param dir_path: directory path
    :param language: language label, must in the config.LANGUAGE_MAPPING
    :param ignore: ignore files can not be dealt with
    :return:
    """
    result = {}
    for file in pathlib.Path(dir_path).iterdir():
        _logger.info(f'processing file: {file}')
        if file.is_dir():
            sub_res = cyclomatic_in_batch(dir_path=str(file))
            result.update(sub_res)
        try:
            block = cyclomatic_singly(str(file), language=language)
            result[str(file)] = block
        except FileNotFoundError:
            if not ignore:
                raise
            else:
                _logger.info(f'ignore {file}')
        except NotImplementedError:
            _logger.info(f'skip(not implemented for {file.suffix}) {file}')
    return result
