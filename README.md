# Multi-Agent Code Review Pipeline


## Project Goal

The goal is to design and implement a fully functional multi-agent artificial intelligence system capable of analyzing source code automatically.

The system accepts user-provided code at runtime and processes it through multiple specialized AI agents. Each agent performs a distinct task such as understanding the code, detecting bugs, suggesting improvements, and generating tests.

The pipeline demonstrates:

* autonomous agent collaboration,
* structured reasoning,
* modular AI architecture,
* automated software engineering workflows.

---

## Project Structure

```
code_review_pipeline/
├── main.py              # Entry point (argparse, interactive input)
├── pipeline.py          # Orchestrator — runs agents, saves logs
├── ui.py                # Rich terminal UI helpers
├── requirements.txt
├── agents/
│   ├── __init__.py
│   ├── base.py              # BaseAgent (API call, JSON parse, trace recording)
│   ├── intent_parser.py     # Agent 1
│   ├── bug_hunter.py        # Agent 2
│   ├── refactor_advisor.py  # Agent 3
│   ├── code_fixer.py        # Agent 4
│   └── test_generator.py    # Agent 5
└── runs/                # Auto-created, one JSON per run
```

---

# System Architecture

The system is composed of four independent AI agents working sequentially.

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
│  Refactor       │  Rates code quality before & after
│  Advisor        │  
└────────┬────────┘
         │ refactor JSON
          ▼
┌─────────────────┐
│  Agent 4        │  Produces corrected code applying all bug fixes
│  Code Fixer     │  and refactoring suggestions
└────────┬────────┘
         │ fixed JSON
         ▼
┌─────────────────┐
│  Agent 5        │  Writes a complete runnable test suite
│  Test Generator │  Regression tests for every bug found
└────────┬────────┘
         │
         ▼
  Final Report  +  runs/<timestamp>.json
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

---

## 2. Bug Hunter Agent

### Role

Detects logical, runtime, and structural issues in the code.

### Responsibilities

* Find runtime errors
* Detect unsafe operations
* Identify bad practices
* Classify issues by severity

---

## 3. Refactor Advisor Agent

### Role

Suggests improvements for readability, maintainability, and style.

### Responsibilities

* Improve readability
* Suggest better naming
* Recommend structural refactoring
* Estimate quality improvement

---

## 4. Code Fixer Agent

### Role

Produces a corrected version of the code based on all prior agents' findings.

### Responsibilities

* Apply bug fixes identified by the Bug Hunter
* Incorporate refactoring suggestions from the Refactor Advisor
* Return complete, corrected source code
* Document each change with type, description, and reason
* List any remaining limitations

---

## 5. Test Generator Agent

### Role

Automatically generates test cases for the fixed code.

### Responsibilities

* Generate unit tests
* Create edge-case scenarios
* Suggest testing frameworks
* Improve code coverage

---

# Technologies Used

* Python 3.13
* OpenAI API
* GPT-4o-mini
* Rich (terminal UI)

---

# Run Instructions

There are 3 options to use the agent:

Run the application:

```bash
# 1. Interactive
python main.py
```

Paste code into the terminal.

Finish input with:

```text
END
```

```bash
# 2. Review a file directly
python main.py --file path/to/mycode.py
```
```bash
# 3. Run with built-in buggy sample
python main.py --demo
```


---

# Example Input

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
END
```

# Example Output

The system generates:

* intent analysis,
* bug reports,
* refactoring suggestions,
* fixed code with change log,
* generated tests,
* structured final report.

```json
{
  "timestamp": "...",
  "user_input": "...the code...",
  "agents": [
    {
      "agent_name": "Code Analyst",
      "role": "...",
      "system_prompt": "...",
      "user_message": "...",
      "response": "..."
    },
    ...
  ],
  "final_answer": "..."
}
```

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
* corrected code with change log,
* generated unit tests,
* testing framework suggestions,
* final summarized report.

---

# Limitations

* Depends on external API availability
* Limited by model context length
* May generate incorrect suggestions for very complex code
* Currently optimized mainly for Python
* Does not execute code safely in sandboxed environments
* No GUI/web interface

---

# Possible Improvements

## Technical Improvements

* Add execution sandbox
* Add syntax highlighting
* Add streaming responses
* Add caching system

## AI Improvements

* Add security audit agent
* Add performance optimization agent
* Add quality checking agent
* Add memory between agents
* Add confidence scoring

## UI Improvements

* Web interface
* Export reports to PDF

---