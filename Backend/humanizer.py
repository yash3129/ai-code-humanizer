import re
import subprocess
import os
from humanizer_ast.python_ast import humanize_python_ast

def rename_variables(code: str, replacements: dict) -> str:
    for old, new in replacements.items():
        code = re.sub(rf'\b{old}\b', new, code)
    return code

def add_inline_comments(code: str, language: str) -> str:
    lines = code.split('\n')
    commented = []

    for line in lines:
        l = line.strip()
        if l.startswith("for"):
            comment = "  # Looping over items" if language == "python" else "  // Looping over items"
            commented.append(line + comment)
        elif l.startswith("if"):
            comment = "  # Conditional check" if language == "python" else "  // Conditional check"
            commented.append(line + comment)
        elif "=" in l and not l.startswith(("def", "function", "class", "public", "private", "protected")):
            comment = "  # Variable assignment" if language == "python" else "  // Variable assignment"
            commented.append(line + comment)
        else:
            commented.append(line)
    return '\n'.join(commented)

def generate_docstrings(code: str) -> str:
    pattern = r'def\s+(\w+)\((.*?)\):'
    matches = list(re.finditer(pattern, code))
    for match in matches:
        func_name = match.group(1)
        params = match.group(2)
        docstring = f'    """\n    {func_name} function.\n    Parameters: {params}\n    """'
        insert_pos = match.end()
        code = code[:insert_pos] + "\n" + docstring + code[insert_pos:]
    return code

def humanize_python(code: str) -> str:
    replacements = {
        "x": "total",
        "y": "count",
        "z": "index",
        "temp": "result",
        "a": "value_a",
        "b": "value_b"
    }
    renamed = rename_variables(code, replacements)
    with_comments = add_inline_comments(renamed, "python")
    with_docstring = generate_docstrings(with_comments)
    return with_docstring

def humanize_js(code: str) -> str:
    replacements = {
        "x": "totalSum",
        "y": "countVal",
        "z": "loopIndex",
        "a": "valueA",
        "b": "valueB",
        "temp": "tempResult",
        "i": "index"
    }
    renamed = rename_variables(code, replacements)
    commented = add_inline_comments(renamed, "js")

    pattern = r'function\s+(\w+)\s*\((.*?)\)\s*\{'
    matches = list(re.finditer(pattern, commented))
    for match in matches:
        func = match.group(1)
        params = match.group(2)
        doc = f"// Function: {func}\n// Parameters: {params}\n"
        commented = commented.replace(match.group(0), doc + match.group(0), 1)

    return commented

def humanize_code(code: str, language: str) -> str:
    language = language.lower()

    if language == "python":
        return humanize_python_ast(code)

    elif language == "java":
        os.makedirs("humanizer_ast", exist_ok=True)

        clean_code = re.sub(r'^\s*package\s+[\w\.]+;\s*', '', code, flags=re.MULTILINE)

        with open("humanizer_ast/Test.java", "w", encoding="utf-8") as f:
            f.write(clean_code)

        result = subprocess.run(
            ["java", "-cp", ".;javaparser-core-3.23.1.jar", "JavaHumanizer"],
            cwd="humanizer_ast",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return f"# Error: Java humanization failed\n{result.stderr}"

        if result.stdout.strip() == "":
            return "# Error: Empty response from JavaHumanizer"

        return result.stdout.strip()

    elif language in ["javascript", "js"]:
        return humanize_js(code)

    elif language in ["cpp", "c++"]:
        with open("test.cpp", "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(["python", "humanizer_ast/cpp_ast.py"], capture_output=True, text=True)
        if result.returncode != 0:
            return f"# Error: C++ humanization failed\n{result.stderr}"
        if result.stdout.strip() == "":
            return "# Error: No output from cpp_ast.py"
        return result.stdout

    else:
        return f"# Error: Language '{language}' not supported."