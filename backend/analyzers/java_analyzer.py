import re


def analyze_java_code(code: str):
    """
    Static analyzer for Java code.

    Detects:
    - Syntax validity (basic structural checks)
    - Lines of code
    - Loops
    - Nested loop depth
    - Time complexity
    - Space complexity
    - Functions / methods
    - Classes
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
    # BASIC JAVA SYNTAX CHECK
    # =========================================================

    syntax = "Valid"
    syntax_error = None

    # Balanced braces
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
    # CALCULATE LOOP DEPTH
    # =========================================================
    #
    # We scan the source line by line.
    #
    # Example:
    #
    # for (...) {        depth = 1
    #     for (...) {    depth = 2
    #         ...
    #     }              depth = 1
    # }                  depth = 0
    #
    # =========================================================

    current_depth = 0
    max_loop_depth = 0

    inside_loop_stack = []

    for line in lines:

        stripped = line.strip()


        # -----------------------------------------------------
        # Close braces first
        # -----------------------------------------------------

        closing_braces = stripped.count("}")

        for _ in range(closing_braces):

            if inside_loop_stack:

                inside_loop_stack.pop()

                current_depth = max(
                    0,
                    current_depth - 1
                )


        # -----------------------------------------------------
        # Detect for / while loops
        # -----------------------------------------------------

        loop_matches = re.findall(
            r"\b(for|while)\s*\(",
            stripped
        )

        for _ in loop_matches:

            current_depth += 1

            inside_loop_stack.append(
                "loop"
            )

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

            inside_loop_stack.append(
                "loop"
            )

            max_loop_depth = max(
                max_loop_depth,
                current_depth
            )


        # -----------------------------------------------------
        # Handle braces that are closed on the same line
        # -----------------------------------------------------

        extra_closing = (
            stripped.count("}")
            - len(loop_matches)
        )

        if extra_closing > 0:

            for _ in range(extra_closing):

                if inside_loop_stack:

                    inside_loop_stack.pop()

                    current_depth = max(
                        0,
                        current_depth - 1
                    )


    # =========================================================
    # FALLBACK LOOP DEPTH
    # =========================================================
    #
    # For common Java formatting:
    #
    # for (...) {
    #     for (...) {
    #     }
    # }
    #
    # The above algorithm gives the correct result.
    #
    # If loops exist but depth somehow wasn't detected,
    # use the number of loops as a safe fallback.
    #
    # =========================================================

    if total_loops > 0 and max_loop_depth == 0:

        max_loop_depth = 1


    # =========================================================
    # METHODS / FUNCTIONS
    # =========================================================

    method_pattern = re.compile(
        r"""
        (?:
            public\s+
            |private\s+
            |protected\s+
            |static\s+
            |final\s+
            |synchronized\s+
            |abstract\s+
            |native\s+
            |default\s+
        )*
        [\w<>\[\], ?]+\s+
        \w+\s*
        \([^;{}]*\)
        \s*
        \{
        """,
        re.VERBOSE
    )

    functions = len(
        method_pattern.findall(code)
    )


    # =========================================================
    # CLASSES
    # =========================================================

    classes = len(
        re.findall(
            r"\b(class|interface|enum)\s+\w+",
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


    dynamic_structures = [

        r"\bArrayList\s*<",

        r"\bLinkedList\s*<",

        r"\bHashMap\s*<",

        r"\bHashSet\s*<",

        r"\bTreeMap\s*<",

        r"\bTreeSet\s*<",

        r"\bQueue\s*<",

        r"\bStack\s*<"

    ]


    for pattern in dynamic_structures:

        if re.search(
            pattern,
            code
        ):

            space_complexity = "O(n)"

            break


    # Detect dynamic arrays

    if re.search(
        r"\bnew\s+\w+\s*\[\s*\w+\s*\]",
        code
    ):

        space_complexity = "O(n)"


    # =========================================================
    # CODE SMELLS
    # =========================================================

    code_smells = []


    # ---------------------------------------------------------
    # Deeply nested loops
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
                "Consider optimizing the algorithm or reducing loop nesting."

        })


    # ---------------------------------------------------------
    # Excessive System.out.println
    # ---------------------------------------------------------

    print_count = len(
        re.findall(
            r"System\.out\.println",
            code
        )
    )


    if print_count >= 5:

        code_smells.append({

            "type":
                "Excessive Console Output",

            "severity":
                "Medium",

            "message":
                "Code contains many System.out.println statements.",

            "suggestion":
                "Consider using a logging framework or reducing console output."

        })


    # ---------------------------------------------------------
    # Scanner usage
    # ---------------------------------------------------------

    if re.search(
        r"\bScanner\b",
        code
    ):

        code_smells.append({

            "type":
                "Scanner Usage",

            "severity":
                "Low",

            "message":
                "Scanner is used for input.",

            "suggestion":
                "For performance-sensitive applications, consider BufferedReader."

        })


    # ---------------------------------------------------------
    # Long method detection
    # ---------------------------------------------------------

    method_blocks = re.findall(
        r"\{([^{}]*)\}",
        code,
        re.DOTALL
    )


    for block in method_blocks:

        block_lines = len(
            [
                line
                for line in block.splitlines()
                if line.strip()
            ]
        )


        if block_lines > 50:

            code_smells.append({

                "type":
                    "Long Method",

                "severity":
                    "Medium",

                "message":
                    "A method appears to contain more than 50 lines.",

                "suggestion":
                    "Break the method into smaller, focused methods."

            })

            break


    # =========================================================
    # QUALITY SCORE
    # =========================================================

    quality_score = 100


    if syntax == "Invalid":

        quality_score -= 30


    if max_loop_depth >= 3:

        quality_score -= 20

    elif max_loop_depth == 2:

        quality_score -= 10


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
            classes

    }


    if syntax_error:

        result["error"] = syntax_error


    return result