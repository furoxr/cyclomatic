import pathlib
import cyclomatic


package_path = pathlib.Path(cyclomatic.__file__).parent

# currently supported parser
# Key is the language label.
# Value is the path to the tree-sitter grammar repo ,
# the language name in tree-sitter, and the calculator class
LANGUAGE_MAPPING = {
    'py': [package_path / 'ast' / 'tree-sitter-python', 'python', None]
}
