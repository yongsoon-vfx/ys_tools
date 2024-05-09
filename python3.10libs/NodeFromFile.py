import hou
from pathlib import Path


def createNodeFromFile(file: Path, parent):
    """Creates nodes from a file/string
    Runs the code in the string or file generated from
    Houdini's built-in asCode function.
    **UNSAFE AND ALLOWS ARBITRARY CODE EXECUTION**
    Args:
        file: pathlib.Path or str
            String or path to code to execute
        parent: hou.Node
            Node to create the node under
    """
    code_exc = ""
    locals_t = {}
    if not isinstance(parent, hou.Node):
        raise TypeError(f"{parent} is not of type hou.Node")
    if isinstance(file, str):
        code_exc = file
    elif isinstance(file, Path):
        with open(file, "r") as f:
            code_exc = f.read()
    parent_path = parent.path()
    addcode = f"\na=createNode(hou.node('{parent_path}'))"

    code_exc += addcode

    exec(code_exc, globals(), locals_t)
    output = locals_t["a"]
    return output
