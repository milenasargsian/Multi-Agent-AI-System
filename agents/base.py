"""Base class for all agents in the pipeline."""

import json
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class AgentTrace:
    """
        Single agent's execution structure
    """
    agent_name: str
    system_prompt: str
    user_prompt: str
    raw_response: str
    parsed_result: dict
    duration_seconds: float
    error: str | None = None


class BaseAgent:
    """
        Parent class every agent inherits from.
        Handles: API call, JSON parsing, timing, and trace recording.
    """
    NAME: str = "Base Agent"
    MODEL: str = "gpt-4o-mini"


    def __init__(self):
        self.client = OpenAI()
        self.trace: AgentTrace | None = None


    @property
    def system_prompt(self) -> str:
        raise NotImplementedError


    def build_user_prompt(self, **kwargs) -> str:
        raise NotImplementedError


    def parse_response(self, raw: str) -> dict:
        try:
            clean = raw.strip()

            if clean.startswith("```json"):
                clean = clean.replace("```json", "")

            clean = clean.replace("```", "").strip()

            start = clean.find("{")
            end = clean.rfind("}")

            if start == -1 or end == -1:
                raise ValueError("No JSON object found")

            clean = clean[start:end + 1]

            return json.loads(clean)

        except Exception as e:
            print("\nJSON PARSE FAILED:\n")
            print(e)

            return {
                "_parse_error": str(e),
                "_raw": raw,
            }

    def run(self, **kwargs) -> dict:
        """
            Execute the agent: call the API, parse, record trace.
        """
        user_prompt = self.build_user_prompt(**kwargs)

        start = time.time()
        error = None
        raw = ""
        result = {}

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                                   + "\n\nReturn ONLY valid JSON.",
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.2,
                max_tokens=2048,
            )

            raw = response.choices[0].message.content
            result = self.parse_response(raw)

        except Exception as e:
            error = str(e)

            print("\nERROR:\n")
            print(error)

            result = {
                "_error": error,
                "_raw": raw,
            }

        duration = round(time.time() - start, 2)

        self.trace = AgentTrace(
            agent_name=self.NAME,
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            raw_response=raw,
            parsed_result=result,
            duration_seconds=duration,
            error=error,
        )

        return result