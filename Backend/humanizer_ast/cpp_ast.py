from clang.cindex import Index, Config, CursorKind
import re

Config.set_library_file("C:/Users/chaur/Downloads/clang+llvm-20.1.7-x86_64-pc-windows-msvc/clang+llvm-20.1.7-x86_64-pc-windows-msvc/bin/libclang.dll")

RENAME_MAP = {
    "temp": "result",
    "x": "total",
    "y": "count",
    "z": "index",
    "a": "valueA",
    "b": "valueB"
}

def get_function_name(cursor):
    for node in cursor.get_children():
        if node.kind == CursorKind.FUNCTION_DECL:
            return node.spelling
    return "unknown_function"

def get_variable_renames(cursor):
    renames = {}
    def visit(node):
        if node.kind == CursorKind.VAR_DECL and node.spelling in RENAME_MAP:
            renames[node.spelling] = RENAME_MAP[node.spelling]
        for child in node.get_children():
            visit(child)
    visit(cursor)
    return renames

def apply_full_transformation(code, renames, function_name):
    lines = code.split("\n")
    new_lines = []
    inserted_doc = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if not inserted_doc and f"{function_name}(" in stripped and "{" in stripped:
            doc = f"// Function: {function_name}\n// Description: TODO - Describe what this function does.\n"
            new_lines.append(doc.strip())
            inserted_doc = True

        modified_line = line
        for old, new in renames.items():
            if re.search(rf"\bint\s+{old}\b", line):
                new_lines.append("    // Renamed variable: " + old + " → " + new)
                modified_line = re.sub(rf"\b{old}\b", new, modified_line)
            else:
                modified_line = re.sub(rf"\b{old}\b", new, modified_line)

        if "return " in stripped:
            new_lines.append("    // Return the final computed result")
        if "if" in stripped or "else" in stripped:
            new_lines.append("    // Conditional logic to handle flow")

        new_lines.append(modified_line)

    return "\n".join(new_lines)

def humanize_cpp_ast(filename):
    try:
        index = Index.create()
        tu = index.parse(filename)
    except Exception as e:
        return f"// Failed to parse C++ code: {e}"

    if not tu:
        return "// Failed to load C++ translation unit"

    with open(filename, "r", encoding="utf-8") as f:
        original_code = f.read()

    function_name = get_function_name(tu.cursor)
    renames = get_variable_renames(tu.cursor)

    if not renames and function_name == "unknown_function":
        return "// No humanization possible\n" + original_code

    return apply_full_transformation(original_code, renames, function_name)

if __name__ == "__main__":
    print(humanize_cpp_ast("test.cpp"))