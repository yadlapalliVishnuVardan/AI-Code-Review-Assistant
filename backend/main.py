from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.analyzers.python_analyzer import analyze_python_code
from backend.analyzers.java_analyzer import analyze_java_code
from backend.analyzers.c_analyzer import analyze_c_code
from backend.analyzers.cpp_analyzer import analyze_cpp_code

from backend.ai.code_reviewer import review_code_with_ai


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="AI Code Review Assistant"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request Model
# ---------------------------------------------------------

class CodeRequest(BaseModel):

    code: str
    language: str = "python"


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Code Review Assistant API is running",

        "supported_languages": [
            "python",
            "java",
            "c",
            "cpp"
        ]
    }


# ---------------------------------------------------------
# Review Code
# ---------------------------------------------------------

@app.post("/review")
def review_code(request: CodeRequest):

    code = request.code.strip()

    language = request.language.lower().strip()


    # -----------------------------------------------------
    # Validate
    # -----------------------------------------------------

    if not code:

        return {
            "error": "Code cannot be empty."
        }


    # -----------------------------------------------------
    # Python
    # -----------------------------------------------------

    if language == "python":

        analysis = analyze_python_code(code)


    # -----------------------------------------------------
    # Java
    # -----------------------------------------------------

    elif language == "java":

        analysis = analyze_java_code(code)


    # -----------------------------------------------------
    # C
    # -----------------------------------------------------

    elif language == "c":

        analysis = analyze_c_code(code)


    # -----------------------------------------------------
    # C++
    # -----------------------------------------------------

    elif language in ["cpp", "c++"]:

        analysis = analyze_cpp_code(code)

        language = "cpp"


    # -----------------------------------------------------
    # Unsupported Language
    # -----------------------------------------------------

    else:

        return {
            "error": f"Unsupported language: {language}",

            "supported_languages": [
                "python",
                "java",
                "c",
                "cpp"
            ]
        }


    # -----------------------------------------------------
    # AI Review
    # -----------------------------------------------------

    try:

        ai_review = review_code_with_ai(
            code,
            analysis
        )

    except Exception as e:

        ai_review = (
            "AI review could not be generated.\n\n"
            f"Reason: {str(e)}"
        )


    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return {

        "language": language,

        "analysis": analysis,

        "ai_review": ai_review

    }