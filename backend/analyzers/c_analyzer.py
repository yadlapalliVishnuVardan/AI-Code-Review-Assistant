import re


def analyze_c_code(code: str):
    """
    Static analyzer for C code.

    Detects:
    - Basic syntax validity
    - Lines of code
    - Loops
    - Nested loop depth
    - Time complexity
    - Space complexity
    - Functions
    - Structs
    - Code smells
    - Quality score
    """

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    lines = [
        line
        for line in code.splitlines()
        if line.strip()
    ]

    line_count = len(lines)

    # =========================================================
    # BASIC SYNTAX CHECK
    # =========================================================

    syntax = "Valid"
    syntax_error = None

    # Balanced curly braces
    if code.count("{") != code.count("}"):

        syntax = "Invalid"
        syntax_error = "Unbalanced curly braces."

    # Balanced parentheses
    elif code.count("(") != code.count(")"):

        syntax = "Invalid"
        syntax_error = "Unbalanced parentheses."

    # Balanced square brackets
    elif code.count("[") != code.count("]"):

        syntax = "Invalid"
        syntax_error = "Unbalanced square brackets."

    # =========================================================
    # COUNT LOOPS
    # =========================================================

    for_loops = len(
        re.findall(
            r"\bfor\s*\(",
            code
        )
    )

    while_loops = len(
        re.findall(
            r"\bwhile\s*\(",
            code
        )
    )

    do_while_loops = len(
        re.findall(
            r"\bdo\s*\{",
            code
        )
    )

    total_loops = (
        for_loops
        + while_loops
        + do_while_loops
    )

    # =========================================================
    # LOOP DEPTH
    # =========================================================

    current_depth = 0
    max_loop_depth = 0

    loop_stack = []

    for line in lines:

        stripped = line.strip()

        # -----------------------------------------------------
        # Close loops when braces close
        # -----------------------------------------------------

        closing_braces = stripped.count("}")

        for _ in range(closing_braces):

            if loop_stack:

                loop_stack.pop()

                current_depth = max(
                    0,
                    current_depth - 1
                )

        # -----------------------------------------------------
        # Detect for / while
        # -----------------------------------------------------

        loop_matches = re.findall(
            r"\b(for|while)\s*\(",
            stripped
        )

        for _ in loop_matches:

            current_depth += 1

            loop_stack.append("loop")

            max_loop_depth = max(
                max_loop_depth,
                current_depth
            )

        # -----------------------------------------------------
        # Detect do-while
        # -----------------------------------------------------

        if re.search(
            r"\bdo\s*\{",
            stripped
        ):

            current_depth += 1

            loop_stack.append("loop")

            max_loop_depth = max(
                max_loop_depth,
                current_depth
            )

    # =========================================================
    # FALLBACK
    # =========================================================

    if total_loops > 0 and max_loop_depth == 0:

        max_loop_depth = 1

    # =========================================================
    # FUNCTIONS
    # =========================================================

    # Typical C function:
    #
    # int add(int a, int b) {
    #
    # void display() {
    #

    function_pattern = re.compile(
        r"""
        (?:
            static\s+
            |extern\s+
            |inline\s+
            |const\s+
        )*
        [A-Za-z_][A-Za-z0-9_\s\*]*
        \s+
        [A-Za-z_][A-Za-z0-9_]*
        \s*
        \([^;{}]*\)
        \s*
        \{
        """,
        re.VERBOSE
    )

    functions = len(
        function_pattern.findall(code)
    )

    # Don't count common control statements
    control_keywords = {
        "if",
        "for",
        "while",
        "switch"
    }

    function_matches = re.findall(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*\{",
        code
    )

    for name in function_matches:

        if name in control_keywords:

            functions -= 1

    functions = max(
        0,
        functions
    )

    # =========================================================
    # STRUCTURES
    # =========================================================

    structs = len(
        re.findall(
            r"\bstruct\s+[A-Za-z_][A-Za-z0-9_]*",
            code
        )
    )

    # =========================================================
    # TIME COMPLEXITY
    # =========================================================

    if max_loop_depth >= 3:

        time_complexity = "O(n³)"

    elif max_loop_depth == 2:

        time_complexity = "O(n²)"

    elif max_loop_depth == 1:

        time_complexity = "O(n)"

    else:

        time_complexity = "O(1)"

    # =========================================================
    # SPACE COMPLEXITY
    # =========================================================

    space_complexity = "O(1)"

    # Detect dynamic memory allocation

    dynamic_memory = [

        r"\bmalloc\s*\(",
        r"\bcalloc\s*\(",
        r"\brealloc\s*\("

    ]

    if any(
        re.search(pattern, code)
        for pattern in dynamic_memory
    ):

        space_complexity = "O(n)"

    # Detect variable-sized arrays

    if re.search(
        r"\b[A-Za-z_][A-Za-z0-9_]*\s+\w+\s*\[\s*[A-Za-z_][A-Za-z0-9_]*\s*\]",
        code
    ):

        space_complexity = "O(n)"

    # =========================================================
    # CODE SMELLS
    # =========================================================

    code_smells = []

    # ---------------------------------------------------------
    # Deep nested loops
    # ---------------------------------------------------------

    if max_loop_depth >= 3:

        code_smells.append({

            "type":
                "Deeply Nested Loops",

            "severity":
                "High",

            "message":
                "Code contains 3 or more nested loops.",

            "suggestion":
                "Consider reducing loop nesting or optimizing the algorithm."

        })

    # ---------------------------------------------------------
    # Excessive printf
    # ---------------------------------------------------------

    printf_count = len(
        re.findall(
            r"\bprintf\s*\(",
            code
        )
    )

    if printf_count >= 5:

        code_smells.append({

            "type":
                "Excessive Console Output",

            "severity":
                "Medium",

            "message":
                "Code contains many printf statements.",

            "suggestion":
                "Reduce unnecessary console output."

        })

    # ---------------------------------------------------------
    # scanf usage
    # ---------------------------------------------------------

    if re.search(
        r"\bscanf\s*\(",
        code
    ):

        code_smells.append({

            "type":
                "scanf Usage",

            "severity":
                "Low",

            "message":
                "The program uses scanf for input.",

            "suggestion":
                "Validate user input carefully to avoid unexpected input issues."

        })

    # ---------------------------------------------------------
    # malloc without free
    # ---------------------------------------------------------

    has_malloc = re.search(
        r"\b(malloc|calloc|realloc)\s*\(",
        code
    )

    has_free = re.search(
        r"\bfree\s*\(",
        code
    )

    if has_malloc and not has_free:

        code_smells.append({

            "type":
                "Possible Memory Leak",

            "severity":
                "High",

            "message":
                "Dynamic memory allocation is used without an obvious free().",

            "suggestion":
                "Ensure dynamically allocated memory is released using free()."

        })

    # ---------------------------------------------------------
    # gets() detection
    # ---------------------------------------------------------

    if re.search(
        r"\bgets\s*\(",
        code
    ):

        code_smells.append({

            "type":
                "Unsafe gets()",

            "severity":
                "High",

            "message":
                "gets() can cause buffer overflow vulnerabilities.",

            "suggestion":
                "Use fgets() with an appropriate buffer size instead."

        })

    # ---------------------------------------------------------
    # Very long code
    # ---------------------------------------------------------

    if line_count > 300:

        code_smells.append({

            "type":
                "Large Source File",

            "severity":
                "Medium",

            "message":
                "The source file contains more than 300 lines.",

            "suggestion":
                "Consider splitting the program into smaller modules."

        })

    # =========================================================
    # QUALITY SCORE
    # =========================================================

    quality_score = 100

    # Syntax problem

    if syntax == "Invalid":

        quality_score -= 30

    # Nested loops

    if max_loop_depth >= 3:

        quality_score -= 20

    elif max_loop_depth == 2:

        quality_score -= 10

    # Code smells

    if len(code_smells) >= 3:

        quality_score -= 15

    elif len(code_smells) == 2:

        quality_score -= 10

    elif len(code_smells) == 1:

        quality_score -= 5

    quality_score = max(
        0,
        quality_score
    )

    # =========================================================
    # FINAL RESULT
    # =========================================================

    result = {

        "syntax":
            syntax,

        "lines":
            line_count,

        "loops":
            total_loops,

        "nested_loops":
            max_loop_depth > 1,

        "loop_depth":
            max_loop_depth,

        "time_complexity":
            time_complexity,

        "space_complexity":
            space_complexity,

        "code_smells":
            code_smells,

        "quality_score":
            quality_score,

        "functions":
            functions,

        "classes":
            structs

    }

    # Add syntax error if present

    if syntax_error:

        result["error"] = syntax_error

    return result