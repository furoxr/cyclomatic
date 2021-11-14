## Feature:

1. calculate cyclomatic complexity of a program (python)
2. generate ast from source code with the help of tree-sitter
3. support the calculation in parallel when the target is a directory

## Introduction:

- python 3.10 required

- The cyclomatic complexity is equal to the num of decision point plus one.
This package use two steps to calculate it:
    1. generates ast from the source code with the help of tree-sitter
    2. walks the ast and counts the num of decesion points

## Examples:


## Concepts:

[Cyclomatic complexity - Wikiwand](https://www.wikiwand.com/en/Cyclomatic_complexity)

[Control-flow graph - Wikiwand](https://www.wikiwand.com/en/Control-flow_graph)

## Resources:

tree-sitter python binding: [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)

tree-sitter python grammer:  [tree-sitter-python](https://github.com/tree-sitter/tree-sitter-python/blob/8600d7fadf5a51b9396eacbc6d105d0649b4c6f6/grammar.js#L73)
