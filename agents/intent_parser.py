"""Agent 1: Intent Parser - understands what the code is supposed to do."""

from agents.base import BaseAgent


class IntentParserAgent(BaseAgent):
    """
        Responsibility: Analyze the raw source code and produce a structured
        description/metadata of its purpose, language, functions, design patterns,
        and complexity level.
    """
    NAME = "Intent Parser"


    @property
    def system_prompt(self) -> str:
        return """\
You are the Intent Parser agent in a multi-agent code review pipeline.

Your ONLY responsibility: analyze the submitted source code and return a \
JSON object describing it.

Return EXACTLY this JSON schema — no preamble, no markdown fences:
{
  "language": "<detected language>",
  "purpose": "<1-2 sentences: what this code does>",
  "functions": ["<name of each function/class/method>"],
  "patterns": ["<design patterns or paradigms used, e.g. callback, singleton>"],
  "complexity": "Low | Medium | High",
  "context": "<inferred domain: e.g. REST API, data processing, CLI tool>",
  "dependencies": ["<external libraries or modules imported>"]
}

Rules:
- Respond ONLY with valid JSON. No text before or after.
- If the code is empty or unparseable, set purpose to "Unable to determine".
- List every distinct function, class, or method in "functions".
"""


    def build_user_prompt(self, code: str, **_) -> str:
        return f"Analyze this code:\n\n```\n{code}\n```"
