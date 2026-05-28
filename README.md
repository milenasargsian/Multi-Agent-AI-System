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