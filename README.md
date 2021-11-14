## Feature:
> python 3.10.0 is required
1. calculate cyclomatic complexity of a program (python)
2. generate ast from source code with the help of tree-sitter
3. support the calculation in parallel when the target is a directory


## Installation

```
pip install git+https://github.com/furoxr/cyclomatic.git
```

## Examples:
```
import pathlib
import cyclomatic
from cyclomatic import (
    cyclomatic_singly,
    cyclomatic_in_batch,
    cyclomatic_in_parallel
)

package_path = pathlib.Path(cyclomatic.__file__).parent

# get the cyclomatic complexity of the whole file
result = cyclomatic_singly(str(package_path / 'cyclomatic.py'))
score_of_the_module = result.score

# get the cyclomatic complexity under the target directory
result = cyclomatic_in_batch(str(package_path))
file_names = list(result.keys())
corresponding_complexity_score = [i.score for i in list(result.values())]

# calculating in parallel would be much more efficient if there are many files
result = cyclomatic_in_parallel(str(package_path))

```

## Introduction:

- The cyclomatic complexity is equal to the num of decision point plus one.
This package use two steps to calculate it:
  1. generates ast from the source code with the help of tree-sitter
  2. walks the ast and counts the num of decesion points

- package structure:
  1. cyclomatic.ast is responsable for ast generation.
  2. cyclomatic.calculator is responsable for calculation of the cyclomatic complexity. every module under this package is a calculator for the target program language. Though it only supports python for now. 


## Concepts:

[Cyclomatic complexity - Wikiwand](https://www.wikiwand.com/en/Cyclomatic_complexity)

[Control-flow graph - Wikiwand](https://www.wikiwand.com/en/Control-flow_graph)

## Resources:

tree-sitter python binding: [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)

tree-sitter python grammer:  [tree-sitter-python](https://github.com/tree-sitter/tree-sitter-python/blob/8600d7fadf5a51b9396eacbc6d105d0649b4c6f6/grammar.js#L73)
