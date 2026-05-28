"""Agent 3: Refactor Advisor - suggests idiomatic improvements and performance gains."""

import json
from agents.base import BaseAgent


class RefactorAdvisorAgent(BaseAgent):
    """
        Responsibility: Suggest concrete code improvements for readability,
        performance, and idiomatic style. Aware of the bugs already found
        so it doesn't duplicate findings — it focuses on non-buggy improvement.
        Produces a before/after quality score and categorized suggestions.
    """
    NAME = "Refactor Advisor"


    @property
    def system_prompt(self) -> str:
        return """\
You are the Refactor Advisor agent in a multi-agent code review pipeline.

You receive:
  1. The source code.
  2. The Intent Parser's structural analysis.
  3. The Bug Hunter's findings (already reported — do NOT repeat them).

Your ONLY responsibility: suggest refactoring improvements that make the code
cleaner, faster, and more idiomatic — beyond the bugs already found.

Return EXACTLY this JSON schema - no preamble, no markdown fences:
{
  "summary": "<one sentence overall refactor assessment>",
  "score": {"before": <1-10 integer>, "after": <1-10 integer>},
  "readability": [
    {"what": "<change to make>", "why": "<reason>", "example": "<brief code snippet or empty string>"}
  ],
  "performance": [
    {"what": "<change to make>", "why": "<reason>", "example": "<brief code snippet or empty string>"}
  ],
  "style": [
    {"what": "<change to make>", "why": "<reason>", "example": "<brief code snippet or empty string>"}
  ]
}

Rules:
- Respond ONLY with valid JSON.
- Use empty arrays [] for categories with no suggestions.
- score.before: honest rating of current code (1=terrible, 10=perfect).
- score.after: estimated rating after applying suggestions.
- Keep example snippets short (≤5 lines). Use empty string "" if no example helps.
- Do NOT re-report the bugs found by Bug Hunter.
"""


    def build_user_prompt(self, code: str, intent: dict, bugs: dict, **_) -> str:
        return (
            f"Source code:\n\n```\n{code}\n```\n\n"
            f"Intent Parser analysis:\n{json.dumps(intent, indent=2)}\n\n"
            f"Bug Hunter findings (already reported - do not repeat):\n{json.dumps(bugs, indent=2)}"
        )
