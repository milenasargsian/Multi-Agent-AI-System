import json
from agents.base import BaseAgent


class CodeFixingAgent(BaseAgent):
    NAME = "Code Fixer"

    @property
    def system_prompt(self) -> str:
        return """
You are a Code-Fixing Agent.

Your job is to produce a corrected version of the user's code based on:
1. the original code,
2. detected bugs,
3. refactoring suggestions.

Return ONLY valid JSON with this structure:

{
  "summary": "short explanation of what was fixed",
  "fixed_code": "complete corrected code",
  "changes": [
    {
      "type": "bug_fix | refactor | safety | style",
      "description": "what changed",
      "reason": "why this change was needed"
    }
  ],
  "remaining_limitations": []
}
"""

    def build_user_prompt(self, code: str, intent: dict, bugs: dict, refactor: dict, **_) -> str:
        return (
            f"Original code:\n\n```\n{code}\n```\n\n"
            f"Intent Parser analysis:\n{json.dumps(intent, indent=2)}\n\n"
            f"Bug Hunter findings:\n{json.dumps(bugs, indent=2)}\n\n"
            f"Refactor Advisor suggestions:\n{json.dumps(refactor, indent=2)}"
        )