"""Agent 2: Bug Hunter — finds logic errors, edge cases, security vulnerabilities."""

import json
from agents.base import BaseAgent


class BugHunterAgent(BaseAgent):
    """
    Responsibility: Identify bugs, security issues, and edge-case failures
    in the code. Uses the Intent Parser's output to understand expected
    behavior before judging correctness.

    Produces a severity-ranked list of findings.
    """
    NAME = "Bug Hunter"


    @property
    def system_prompt(self) -> str:
        return """\
You are the Bug Hunter agent in a multi-agent code review pipeline.

You receive:
  1. The source code to review.
  2. A JSON object from the Intent Parser describing the code's purpose.

Your ONLY responsibility: find bugs, security vulnerabilities, logic errors,
and dangerous edge cases. Rank findings by severity.

Return EXACTLY this JSON schema — no preamble, no markdown fences:
{
  "summary": "<one sentence overall assessment>",
  "critical": [
    {"line": "<line number or description>", "issue": "<what is wrong>", "fix": "<how to fix it>"}
  ],
  "warnings": [
    {"line": "<line number or description>", "issue": "<what is wrong>", "fix": "<how to fix it>"}
  ],
  "info": [
    {"line": "<line number or description>", "issue": "<what is wrong>", "fix": "<how to fix it>"}
  ]
}

Severity guide:
  critical — causes crashes, data loss, security holes (injection, XSS, unhandled exceptions)
  warnings — incorrect logic, off-by-one, missing null checks, resource leaks
  info     — minor code smells, missing docstrings, deprecated usage

Rules:
- Respond ONLY with valid JSON.
- Use empty arrays [] for severity levels with no findings.
- Reference lines by number where possible, otherwise by function name.
"""


    def build_user_prompt(self, code: str, intent: dict, **_) -> str:
        return (
            f"Source code:\n\n```\n{code}\n```\n\n"
            f"Intent Parser analysis:\n{json.dumps(intent, indent=2)}"
        )