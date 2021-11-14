from typing import (
    Union,
    Optional,
    Dict,
    Tuple
)
import os
import multiprocessing
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


def cyclomatic_safely(path: str, language=None) -> Tuple[str, Optional[Block]]:
    """cyclomatic_singly without Exception, return None instead"""
    try:
        block = cyclomatic_singly(path, language=language)
    except NotImplementedError:
        _logger.info(f"skip(not implemented for {path.split('.')[-1]}) {path}")
        return path, None
    return path, block


def cyclomatic_in_batch(dir_path: str, language=None, ignore=True) -> Dict[str, Optional[Block]]:
    """get the cyclomatic complexity list of the source files in the directory

    :param dir_path: directory path
    :param language: language label, must in the config.LANGUAGE_MAPPING
    :param ignore: ignore files can not be dealt with
    :return: Dict with path string as key, with Block as value
    """
    result = {}
    dir_path = pathlib.Path(dir_path)
    for file in dir_path.rglob('*'):
        relative_path = file.relative_to(dir_path)
        if file.is_dir():
            continue
        try:
            block = cyclomatic_singly(str(file), language=language)
            result[str(file)] = block
        except FileNotFoundError:
            if not ignore:
                raise
            else:
                _logger.info(f'ignore {relative_path}')
        except NotImplementedError:
            _logger.info(f'skip(not implemented for {file.suffix}) {relative_path}')
            continue
        _logger.info(f'done file: {relative_path}')
    return result


def cyclomatic_in_parallel(dir_path, worker_num=None) -> Dict[str, Optional[Block]]:
    """work in parallel, not optimized.

    This function is more efficient only when the target directory contains more than dozens of modules.
    :param dir_path: target directory path str
    :param worker_num: num of real executors. By default, there will be workers with the same number of CPU cores.
    :return: a dict with file path as key, and with Block as value
    """

    worker_num = worker_num if worker_num else os.cpu_count()
    files = [str(f) for f in pathlib.Path(dir_path).rglob('*') if f.is_file()]
    with multiprocessing.Pool(worker_num) as pool:
        result = pool.map(cyclomatic_safely, files)
        return {
            i[0]: i[1]
            for i in result
            if i[1]
        }
