"""
    Pipeline orchestrator - runs all 5 agents in sequence,
    collects traces, writes the run log, and prints results.
"""

import json
from datetime import datetime
from pathlib import Path

from agents import (
    IntentParserAgent,
    BugHunterAgent,
    RefactorAdvisorAgent,
    CodeFixingAgent,
    TestGeneratorAgent
)
from ui import UI


RUNS_DIR = Path(__file__).parent / "runs"


class CodeReviewPipeline:
    """
        Orchestrates the 5 agent code review pipeline.
    """

    def run(self, code: str) -> dict:
        UI.banner()
        UI.print(f"[dim]Code length: {len(code.splitlines())} lines · {len(code)} chars[/dim]")

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        traces = []
        results = {}

        # Agent 1: Intent Parser
        UI.agent_start("Intent Parser", 1)
        agent1 = IntentParserAgent()
        intent = agent1.run(code=code)
        results["intent"] = intent
        traces.append(self._trace_dict(agent1.trace))
        UI.show_intent(intent)
        UI.agent_done("Intent Parser")

        # Agent 2: Bug Hunter
        UI.agent_start("Bug Hunter", 2)
        agent2 = BugHunterAgent()
        bugs = agent2.run(code=code, intent=intent)
        results["bugs"] = bugs
        traces.append(self._trace_dict(agent2.trace))
        UI.show_bugs(bugs)
        UI.agent_done("Bug Hunter")

        # Agent 3: Refactor Advisor
        UI.agent_start("Refactor Advisor", 3)
        agent3 = RefactorAdvisorAgent()
        refactor = agent3.run(code=code, intent=intent, bugs=bugs)
        results["refactor"] = refactor
        traces.append(self._trace_dict(agent3.trace))
        UI.show_refactor(refactor)
        UI.agent_done("Refactor Advisor")

        # Agent 4: Code Fixer
        UI.agent_start("Code Fixer", 4)
        agent4 = CodeFixingAgent()
        fixed = agent4.run(code=code, intent=intent, bugs=bugs, refactor=refactor)
        results["fixed"] = fixed
        traces.append(self._trace_dict(agent4.trace))
        UI.show_fixed_code(fixed)
        UI.agent_done("Code Fixer")

        # Agent 5: Test Generator
        UI.agent_start("Test Generator", 5)
        agent5 = TestGeneratorAgent()
        tests = agent5.run(code=fixed.get("fixed_code", code), intent=intent, bugs=bugs, refactor=refactor)
        results["tests"] = tests
        traces.append(self._trace_dict(agent5.trace))
        UI.show_tests(tests)
        UI.agent_done("Test Generator")

        # Final report
        final = self._build_final_report(intent, bugs, refactor, fixed, tests)
        log_path = self._save_run_log(run_id, code, traces, final)
        UI.show_final_report(final, log_path)

        return final


    @staticmethod
    def _trace_dict(trace) -> dict:
        if trace is None:
            return {}

        return {
            "agent": trace.agent_name,
            "duration_seconds": trace.duration_seconds,
            "system_prompt": trace.system_prompt,
            "user_prompt": trace.user_prompt,
            "raw_response": trace.raw_response,
            "parsed_result": trace.parsed_result,
            "error": trace.error
        }


    @staticmethod
    def _build_final_report(intent: dict, bugs: dict, refactor: dict, fixed: dict, tests: dict) -> dict:
        return {
            "language": intent.get("language", "-"),
            "complexity": intent.get("complexity", "-"),
            "purpose": intent.get("purpose", "-"),
            "critical_bugs": len(bugs.get("critical", [])),
            "warnings": len(bugs.get("warnings", [])),
            "info_notes": len(bugs.get("info", [])),
            "quality_before": refactor.get("score", {}).get("before"),
            "quality_after": refactor.get("score", {}).get("after"),
            "code_fixed": bool(fixed.get("fixed_code")),
            "changes_made": len(fixed.get("changes", [])),
            "test_framework": tests.get("framework", "-"),
            "test_scenarios": len(tests.get("coverage", []))
        }


    def _save_run_log(self, run_id: str, code: str, traces: list, final: dict) -> str:
        RUNS_DIR.mkdir(exist_ok=True)
        log = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "user_input": code,
            "agents": traces,
            "final_answer": final
        }

        path = RUNS_DIR / f"{run_id}.json"
        path.write_text(
            json.dumps(log, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return str(path)
