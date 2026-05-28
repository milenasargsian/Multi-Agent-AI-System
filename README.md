# Multi-Agent Code Review Pipeline
**LLM Course Project** — 4 specialized AI agents that analyze source code in sequence.

## Architecture

```
User Input (code)
      │
      ▼
┌─────────────────┐
│  Agent 1        │  Detects language, purpose, functions, patterns, complexity
│  Intent Parser  │
└────────┬────────┘
         │ intent JSON
         ▼
┌─────────────────┐
│  Agent 2        │  Finds critical bugs, warnings, security issues
│  Bug Hunter     │  (uses intent as context)
└────────┬────────┘
         │ bugs JSON
         ▼
┌─────────────────┐
│  Agent 3        │  Suggests readability/performance/style improvements
│  Refactor       │  (aware of bugs already found — no duplication)
│  Advisor        │  Rates code quality before & after
└────────┬────────┘
         │ refactor JSON
         ▼
┌─────────────────┐
│  Agent 4        │  Writes a complete runnable test suite
│  Test Generator │  Regression tests for every bug found
└────────┬────────┘
         │
         ▼
  Final Report  +  runs/<timestamp>.json
```

## Setup

```bash
# 1. Clone / unzip the project
cd code_review_pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API key
export OPENAI_API_KEY=sk-proj-...
```

## Usage

```bash
# Interactive — paste code, type END when done
python main.py

# Review a file directly
python main.py --file path/to/mycode.py

# Run with built-in buggy sample (great for demo)
python main.py --demo
```

## Output

Every run produces:
- **Terminal output** — each agent's result printed immediately after it finishes
- **`runs/<timestamp>.json`** — full structured trace with prompts, responses, and final report

### Run log structure (`runs/YYYYMMDD_HHMMSS.json`)
```json
{
  "run_id": "20240521_143022",
  "timestamp": "2024-05-21T14:30:22.123456",
  "user_input": "<submitted code>",
  "agents": [
    {
      "agent": "Intent Parser",
      "duration_seconds": 2.1,
      "system_prompt": "...",
      "user_prompt": "...",
      "raw_response": "...",
      "parsed_result": { ... },
      "error": null
    },
    ...
  ],
  "final_answer": {
    "language": "Python",
    "complexity": "Medium",
    "critical_bugs": 2,
    "warnings": 1,
    "quality_before": 4,
    "quality_after": 8,
    "test_framework": "pytest",
    "test_scenarios": 9
  }
}
```

## Project Structure

```
code_review_pipeline/
├── main.py              # Entry point (argparse, interactive input)
├── pipeline.py          # Orchestrator — runs agents, saves logs
├── ui.py                # Rich terminal UI helpers
├── requirements.txt
├── agents/
│   ├── __init__.py
│   ├── base.py          # BaseAgent (API call, JSON parse, trace recording)
│   ├── intent_parser.py # Agent 1
│   ├── bug_hunter.py    # Agent 2
│   ├── refactor_advisor.py  # Agent 3
│   └── test_generator.py    # Agent 4
└── runs/                # Auto-created, one JSON per run
```

## Sample Code (built into --demo)

The demo uses buggy JavaScript-style Python that contains:
- Off-by-one error in `process_orders` (`range(len + 1)` → IndexError)
- XSS risk in `fetch_user_data` (string concatenation into HTML)
- Missing return-value checks in `find_user` (implicit None)
- No error handling on HTTP requests


# Autonomous Multi-Agent Code Review Pipeline

## Project Title

Autonomous Multi-Agent Code Review Pipeline

---

## Selected Domain

Artificial Intelligence / Software Engineering / Automated Code Analysis

---

## Project Goal

The goal of this project is to design and implement a fully functional multi-agent artificial intelligence system capable of analyzing source code automatically.

The system accepts user-provided code at runtime and processes it through multiple specialized AI agents. Each agent performs a distinct task such as understanding the code, detecting bugs, suggesting improvements, and generating tests.

The pipeline demonstrates:

* autonomous agent collaboration,
* structured reasoning,
* modular AI architecture,
* automated software engineering workflows.

---

# System Architecture

The system is composed of four independent AI agents working sequentially.

```text
User Code Input
       ↓
Intent Parser Agent
       ↓
Bug Hunter Agent
       ↓
Refactor Advisor Agent
       ↓
Test Generator Agent
       ↓
Final Structured Report
```

---

# Agent List and Responsibilities

## 1. Intent Parser Agent

### Role

Analyzes the input code and extracts high-level information.

### Responsibilities

* Detect programming language
* Determine code complexity
* Understand code purpose
* Extract functions and patterns
* Identify context and dependencies

### Output Example

* Language: Python
* Complexity: Low
* Functions: divide()

---

## 2. Bug Hunter Agent

### Role

Detects logical, runtime, and structural issues in the code.

### Responsibilities

* Find runtime errors
* Detect unsafe operations
* Identify bad practices
* Classify issues by severity

### Output Example

* Division by zero
* Null reference risks
* Infinite loops

---

## 3. Refactor Advisor Agent

### Role

Suggests improvements for readability, maintainability, and style.

### Responsibilities

* Improve readability
* Suggest better naming
* Recommend structural refactoring
* Estimate quality improvement

### Output Example

* Add docstrings
* Use descriptive variable names
* Add error handling

---

## 4. Test Generator Agent

### Role

Automatically generates test cases for the input code.

### Responsibilities

* Generate unit tests
* Create edge-case scenarios
* Suggest testing frameworks
* Improve code coverage

### Output Example

* pytest test suite
* edge case validation
* exception testing

---

# Technologies Used

* Python 3.13
* OpenAI API
* GPT-4o-mini
* Rich (terminal UI)
* python-dotenv

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
cd code_review_pipeline
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# Run Instructions

Run the application:

```bash
python main.py
```

Paste code into the terminal.

Finish input with:

```text
END
```

---

# Example Input

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
END
```

---

# Example Output

The system generates:

* intent analysis,
* bug reports,
* refactoring suggestions,
* generated tests,
* structured final report.

---

# Input Description

The system accepts:

* Python code
* Function definitions
* Scripts
* Algorithm implementations

Input is provided through terminal interaction.

---

# Output Description

The pipeline returns:

* detected language,
* code complexity,
* identified bugs,
* quality scores,
* readability improvements,
* generated unit tests,
* testing framework suggestions,
* final summarized report.

---

# Project Features

* Multi-agent AI architecture
* Autonomous agent collaboration
* Structured JSON communication
* Runtime code analysis
* AI-generated testing
* Rich terminal interface
* Persistent run logs

---

# Limitations

* Depends on external API availability
* Limited by model context length
* May generate incorrect suggestions for very complex code
* Currently optimized mainly for Python
* Does not execute code safely in sandboxed environments
* No GUI/web interface yet

---

# Possible Improvements

## Technical Improvements

* Add AST-based static analysis
* Add execution sandbox
* Add syntax highlighting
* Add streaming responses
* Add parallel agent execution
* Add caching system

## AI Improvements

* Add security audit agent
* Add performance optimization agent
* Add code-fixing agent
* Add memory between agents
* Add confidence scoring

## UI Improvements

* Web interface using Streamlit or Gradio
* Export reports to PDF
* Interactive dashboard
* Real-time visualization

---

# Conclusion

This project demonstrates how multiple AI agents can collaborate autonomously to solve complex software engineering tasks.

The system combines:

* intelligent reasoning,
* structured analysis,
* automated testing,
* and modular AI orchestration

into a practical and extensible code review pipeline.
