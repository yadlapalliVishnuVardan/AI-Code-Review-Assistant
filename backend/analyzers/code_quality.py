import ast


def detect_code_smells(tree):

    smells = []

    # Check nested loops
    max_loop_depth = find_loop_depth(tree)

    if max_loop_depth >= 3:
        smells.append({
            "type": "Deeply Nested Loops",
            "severity": "High",
            "message": "Code contains 3 or more nested loops.",
            "suggestion": "Consider optimizing the algorithm or reducing loop nesting."
        })

    # Check number of functions
    function_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1

    if function_count > 10:
        smells.append({
            "type": "Too Many Functions",
            "severity": "Medium",
            "message": "The file contains many functions.",
            "suggestion": "Consider splitting the code into multiple modules."
        })

    return smells


def find_loop_depth(node, current_depth=0):

    max_depth = current_depth

    if isinstance(node, (ast.For, ast.While)):
        current_depth += 1
        max_depth = current_depth

    for child in ast.iter_child_nodes(node):

        child_depth = find_loop_depth(
            child,
            current_depth
        )

        max_depth = max(max_depth, child_depth)

    return max_depth