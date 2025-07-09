import ast
import astunparse
import re

RENAME_MAP = {
    "x": "total_sum",
    "y": "counter",
    "z": "index",
    "temp": "result",
    "a": "value_a",
    "b": "value_b"
}

class PythonVariableRenamer(ast.NodeTransformer):
    def __init__(self, mapping):
        self.mapping = mapping
        self.renamed_vars = {}

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)) and node.id in self.mapping:
            self.renamed_vars[node.id] = self.mapping[node.id]
            return ast.copy_location(ast.Name(id=self.mapping[node.id], ctx=node.ctx), node)
        return node

    def visit_arg(self, node):
        if node.arg in self.mapping:
            self.renamed_vars[node.arg] = self.mapping[node.arg]
            node.arg = self.mapping[node.arg]
        return node

def insert_docstring_and_comments(code, func_name, args, renamed_vars):
    lines = code.split("\n")
    new_lines = []
    docstring = f'    """\n    Function: {func_name}\n    Parameters: {", ".join(args)}\n    Description: TODO - Describe what this function does.\n    """'
    inserted_doc = False

    for line in lines:
        stripped = line.strip()
        if not inserted_doc and stripped.startswith("def ") and func_name in stripped:
            new_lines.append(line)
            new_lines.append(docstring)
            inserted_doc = True
            continue

        for original, new in renamed_vars.items():
            if re.search(rf"\b{new}\s*=", line):
                new_lines.append(f"    # Renamed '{original}' to '{new}'")
                break

        if "return " in stripped:
            new_lines.append("    # Return the computed result")

        new_lines.append(line)

    return "\n".join(new_lines)

def humanize_python_ast(code: str) -> str:
    try:
        tree = ast.parse(code)
        transformer = PythonVariableRenamer(RENAME_MAP)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        new_code = astunparse.unparse(tree)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                args = [arg.arg for arg in node.args.args]
                return insert_docstring_and_comments(new_code, func_name, args, transformer.renamed_vars)

        return new_code

    except Exception as e:
        return f"# Failed to humanize with AST: {e}"

if __name__ == "__main__":
    with open("test.py", "r") as f:
        code = f.read()
    print(humanize_python_ast(code))