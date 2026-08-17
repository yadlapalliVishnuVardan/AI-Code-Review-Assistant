# 🤖 AI Code Review Assistant

An AI-powered code review web application that analyzes source code, detects potential code-quality issues, estimates time and space complexity, calculates a quality score, and generates an AI-based code review.

## 🚀 Features

- 🔍 Static code analysis
- 🤖 AI-powered code review
- 📊 Code quality score
- ⏱️ Time complexity estimation
- 💾 Space complexity estimation
- 🔁 Loop detection and loop-depth analysis
- ⚠️ Code-smell detection
- 🐍 Python code analysis
- ☕ Java code analysis
- 🇨 C code analysis
- ⚡ C++ code analysis
- 🌐 Web-based frontend
- ⚡ FastAPI backend
- 🔐 Environment variables protected using `.env`

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI

- AI-powered code review

### Frontend

- HTML
- CSS
- JavaScript

### Supported Languages

- Python
- Java
- C
- C++

---

## 📁 Project Structure

```text
AI-Code-Review-Assistant/
│
├── backend/
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   └── code_reviewer.py
│   │
│   ├── analyzers/
│   │   ├── c_analyzer.py
│   │   ├── code_quality.py
│   │   ├── cpp_analyzer.py
│   │   ├── java_analyzer.py
│   │   ├── python_analyzer.py
│   │   └── quality_score.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── test_env.py
│   └── text_analyzer.py
│
├── frontend/
│   └── index.html
│
├── tests/
│
├── .gitignore
└── README.md
