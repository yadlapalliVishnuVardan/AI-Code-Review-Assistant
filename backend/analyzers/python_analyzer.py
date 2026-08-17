from backend.analyzers.code_quality import detect_code_smells
from backend.analyzers.quality_score import calculate_quality_score
import ast

def estimate_space_complexity(tree):

    space_complexity = "O(1)"

    for node in ast.walk(tree):

        # Lists created with [0] * n
        if isinstance(node, ast.List):

            space_complexity = "O(n)"

        # List comprehensions
        elif isinstance(node, ast.ListComp):

            space_complexity = "O(n)"

        # Sets
        elif isinstance(node, ast.Set):

            space_complexity = "O(n)"

        # Dictionaries
        elif isinstance(node, ast.Dict):

            space_complexity = "O(n)"

    return space_complexity
def analyze_python_code(code: str):

    result = {
        "syntax": "Valid",
        "lines": len(code.splitlines()),
        "loops": 0,
        "nested_loops": False,
        "loop_depth": 0,
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "code_smells": [],
        "quality_score": 0,
        "functions": 0,
        "classes": 0
    }

    # Step 1: Parse the code
    try:
        tree = ast.parse(code)
        result["code_smells"] = detect_code_smells(tree)
        result["space_complexity"] = estimate_space_complexity(tree)

    except SyntaxError as error:
        return {
            "syntax": "Invalid",
            "error": error.msg,
            "line": error.lineno
        }

    # Step 2: Count loops, functions and classes
    for node in ast.walk(tree):

        if isinstance(node, (ast.For, ast.While)):
            result["loops"] += 1

        elif isinstance(node, ast.FunctionDef):
            result["functions"] += 1

        elif isinstance(node, ast.ClassDef):
            result["classes"] += 1

    # Step 3: Find maximum nested loop depth
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

    result["loop_depth"] = find_loop_depth(tree)

    # Step 4: Determine whether loops are nested
    if result["loop_depth"] >= 2:
        result["nested_loops"] = True

    # Step 5: Estimate time complexity
    depth = result["loop_depth"]

    if depth == 0:
        result["time_complexity"] = "O(1)"

    elif depth == 1:
        result["time_complexity"] = "O(n)"

    elif depth == 2:
        result["time_complexity"] = "O(n²)"

    elif depth == 3:
        result["time_complexity"] = "O(n³)"

    else:
        result["time_complexity"] = f"O(n^{depth})"

# Code smell analysis
    result["code_smells"] = detect_code_smells(tree)

    # Calculate quality score
    result["quality_score"] = calculate_quality_score(result)

    return result