import pytest
import cyclomatic
import pathlib
from cyclomatic import (
    cyclomatic_singly,
    cyclomatic_in_batch,
    cyclomatic_in_parallel
)


package_path = pathlib.Path(cyclomatic.__file__).parent


def test_cyclomatic_signle():
    # test single file path as input
    result = cyclomatic_singly(str(package_path / 'cyclomatic.py'))
    assert result


def test_cyclomatic_in_batch():
    # test a directory path as input
    result = cyclomatic_in_batch(str(package_path))
    assert result


def test_cyclomatic_in_parallel():
    # test run in parallel
    result_in_batch = cyclomatic_in_batch(str(package_path))
    result_in_parallel = cyclomatic_in_parallel(str(package_path))

    for key, value in result_in_batch.items():
        assert key in result_in_parallel
        assert value == result_in_parallel[key]
