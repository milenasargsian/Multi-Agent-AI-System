"""Agent 4: Test Generator — writes unit tests covering normal and edge cases."""

import json
from agents.base import BaseAgent


class TestGeneratorAgent(BaseAgent):
    """
    Responsibility: Write a complete, runnable test suite for the submitted code.
    Uses all prior agents' outputs to ensure:
      - Normal behavior is tested.
      - Every critical/warning bug found has a regression test.
      - Edge cases inferred from the code structure are covered.

    Produces a self-contained test file and coverage summary.
    """
    NAME = "Test Generator"

    @property
    def system_prompt(self) -> str:
        return """\
You are the Test Generator agent in a multi-agent code review pipeline.

You receive:
  1. The source code.
  2. The Intent Parser's structural analysis.
  3. The Bug Hunter's findings.
  4. The Refactor Advisor's suggestions.

Your ONLY responsibility: write a complete, runnable unit test suite for the code.
Each critical and warning bug must have at least one regression test.

Return EXACTLY this JSON schema — no preamble, no markdown fences:
{
  "framework": "<test framework, e.g. pytest, unittest, Jest>",
  "tests": "<full test file content as a single string — use actual newlines>",
  "coverage": ["<scenario 1>", "<scenario 2>", "..."],
  "notes": "<any setup instructions or caveats>"
}

Rules:
- Respond ONLY with valid JSON.
- Choose the most appropriate framework for the detected language.
- "tests" must be a complete, self-contained file someone can run immediately.
- For Python use pytest style (no class required, plain test_ functions).
- Include a test for every function identified by the Intent Parser.
- Include regression tests for every critical and warning bug found.
- Include at least two edge-case tests (empty input, None, zero, boundary values).
- "coverage" is a human-readable list of what each test verifies.
"""


    def build_user_prompt(self, code: str, intent: dict, bugs: dict, refactor: dict, **_) -> str:
        return (
            f"Source code:\n\n```\n{code}\n```\n\n"
            f"Intent Parser:\n{json.dumps(intent, indent=2)}\n\n"
            f"Bug Hunter:\n{json.dumps(bugs, indent=2)}\n\n"
            f"Refactor Advisor:\n{json.dumps(refactor, indent=2)}"
        )
