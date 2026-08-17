import re


def analyze_cpp_code(code: str):
    """
    Static analyzer for C++ code.

    Detects:
    - Basic syntax validity
    - Lines of code
    - Loops
    - Nested loop depth
    - Time complexity
    - Space complexity
    - Functions
    - Classes / structs
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

    if code.count("{") != code.count("}"):

        syntax = "Invalid"
        syntax_error = "Unbalanced curly braces."

    elif code.count("(") != code.count(")"):

        syntax = "Invalid"
        syntax_error = "Unbalanced parentheses."

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
        # Close braces
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
        # for / while loops
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
        # do-while
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

    # Examples:
    #
    # int add(int a, int b) {
    #
    # void display() {
    #
    # string getName() {
    #
    # C++ methods can also contain:
    #
    # std::string Person::getName() {

    function_pattern = re.compile(
        r"""
        (?:
            static\s+
            |inline\s+
            |virtual\s+
            |const\s+
            |constexpr\s+
            |friend\s+
            |extern\s+
            |explicit\s+
        )*
        [A-Za-z_][A-Za-z0-9_:<>\*&\s]*
        \s+
        [A-Za-z_][A-Za-z0-9_:~]*
        \s*
        \([^;{}]*\)
        \s*
        (?:const\s*)?
        \{
        """,
        re.VERBOSE
    )

    functions = len(
        function_pattern.findall(code)
    )

    # ---------------------------------------------------------
    # Remove common control statements
    # ---------------------------------------------------------

    control_keywords = {
        "if",
        "for",
        "while",
        "switch",
        "catch"
    }

    function_matches = re.findall(
        r"\b([A-Za-z_][A-Za-z0-9_:~]*)\s*\([^;{}]*\)\s*\{",
        code
    )

    for name in function_matches:

        simple_name = name.split("::")[-1]

        if simple_name in control_keywords:

            functions -= 1

    functions = max(
        0,
        functions
    )

    # =========================================================
    # CLASSES / STRUCTS
    # =========================================================

    classes = len(
        re.findall(
            r"\bclass\s+[A-Za-z_][A-Za-z0-9_]*",
            code
        )
    )

    structs = len(
        re.findall(
            r"\bstruct\s+[A-Za-z_][A-Za-z0-9_]*",
            code
        )
    )

    total_classes = classes + structs

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

    # ---------------------------------------------------------
    # Dynamic memory
    # ---------------------------------------------------------

    dynamic_memory_patterns = [

        r"\bnew\s+",

        r"\bmalloc\s*\(",

        r"\bcalloc\s*\(",

        r"\brealloc\s*\("

    ]

    if any(
        re.search(pattern, code)
        for pattern in dynamic_memory_patterns
    ):

        space_complexity = "O(n)"

    # ---------------------------------------------------------
    # STL containers
    # ---------------------------------------------------------

    stl_containers = [

        r"\bvector\s*<",

        r"\blist\s*<",

        r"\bdeque\s*<",

        r"\bqueue\s*<",

        r"\bstack\s*<",

        r"\bset\s*<",

        r"\bmap\s*<",

        r"\bunordered_map\s*<",

        r"\bunordered_set\s*<"

    ]

    if any(
        re.search(pattern, code)
        for pattern in stl_containers
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
    # Excessive cout
    # ---------------------------------------------------------

    cout_count = len(
        re.findall(
            r"\bcout\s*<<",
            code
        )
    )

    if cout_count >= 5:

        code_smells.append({

            "type":
                "Excessive Console Output",

            "severity":
                "Medium",

            "message":
                "Code contains many cout statements.",

            "suggestion":
                "Reduce unnecessary console output."

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
    # scanf
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
                "Validate user input carefully."

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
    # new without delete
    # ---------------------------------------------------------

    has_new = re.search(
        r"\bnew\s+",
        code
    )

    has_delete = re.search(
        r"\bdelete\s+",
        code
    )

    if has_new and not has_delete:

        code_smells.append({

            "type":
                "Possible Memory Leak",

            "severity":
                "Medium",

            "message":
                "new is used without an obvious delete.",

            "suggestion":
                "Prefer RAII and smart pointers such as std::unique_ptr or std::shared_ptr."

        })

    # ---------------------------------------------------------
    # gets()
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
                "Use std::getline() or another bounded input method."

        })

    # ---------------------------------------------------------
    # using namespace std
    # ---------------------------------------------------------

    if re.search(
        r"\busing\s+namespace\s+std\s*;",
        code
    ):

        code_smells.append({

            "type":
                "Global using namespace std",

            "severity":
                "Low",

            "message":
                "using namespace std is used globally.",

            "suggestion":
                "Prefer explicit std:: prefixes, especially in header files."

        })

    # ---------------------------------------------------------
    # Very large source file
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

    # Syntax issue

    if syntax == "Invalid":

        quality_score -= 30

    # Loop complexity

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
            total_classes

    }

    # Add syntax error if present

    if syntax_error:

        result["error"] = syntax_error

    return result