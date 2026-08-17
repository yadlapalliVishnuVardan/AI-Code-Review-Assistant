import ollama


def review_code_with_ai(code, analysis):
    prompt = f"""
You are an expert Python code reviewer.

Analyze the following Python code.

CODE:
{code}

STATIC ANALYSIS:
{analysis}

Provide a clear code review.

Return the following sections:

1. Summary
Explain what the code does.

2. Bugs
List any possible bugs.
If there are no bugs, say "No obvious bugs found."

3. Performance
Explain the time and space complexity.
Suggest ways to improve performance.

4. Code Quality
Identify readability, maintainability, or code-smell issues.

5. Suggestions
Give practical improvements.

6. Optimized Code
Provide an improved version of the code.
If the code is already good, explain why.
"""

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]