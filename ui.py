"""
    Terminal UI helpers using the Rich library
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.rule import Rule
from rich import box

console = Console()


class UI:
    AGENT_STYLES = {
        "Intent Parser":    ("bright_blue",   "🔍"),
        "Bug Hunter":       ("bright_red",    "🐛"),
        "Refactor Advisor": ("bright_yellow", "⚡"),
        "Code Fixer":       ("bright_magenta", "🔧"),
        "Test Generator":   ("bright_green",  "✅")
    }


    @staticmethod
    def banner():
        console.print()
        console.print(Panel.fit(
            "[bold white]Multi-Agent Code Review Pipeline[/bold white]\n"
            "[dim]Intent Parser → Bug Hunter → Refactor Advisor → Code Fixer → Test Generator[/dim]",
            border_style="bright_blue",
            padding=(1, 4),
        ))
        console.print()


    @staticmethod
    def print(*args, **kwargs):
        console.print(*args, **kwargs)


    @staticmethod
    def error(msg: str):
        console.print(f"[bold red]✗ Error:[/bold red] {msg}")


    @staticmethod
    def agent_start(name: str, index: int):
        color, icon = UI.AGENT_STYLES.get(name, ("white", "•"))
        console.print()
        console.print(Rule(
            f"[bold {color}]{icon}  AGENT {index} - {name.upper()}[/bold {color}]",
            style=color,
        ))


    @staticmethod
    def agent_done(name: str):
        color, icon = UI.AGENT_STYLES.get(name, ("white", "•"))
        console.print(f"[{color}]✓ {name} complete[/{color}]")


    @staticmethod
    def show_intent(result: dict):
        table = Table(box=box.SIMPLE_HEAVY, show_header=False, padding=(0, 1))
        table.add_column("Key", style="dim", width=16)
        table.add_column("Value", style="bright_white")
        table.add_row("Language", result.get("language", "—"))
        table.add_row("Complexity", result.get("complexity", "—"))
        table.add_row("Purpose", result.get("purpose", "—"))
        table.add_row("Context", result.get("context", "—"))
        funcs = ", ".join(result.get("functions", [])) or "-"
        table.add_row("Functions", funcs)
        patterns = ", ".join(result.get("patterns", [])) or "-"
        table.add_row("Patterns", patterns)
        console.print(table)


    @staticmethod
    def show_bugs(result: dict):
        console.print(f"[italic dim]{result.get('summary', '')}[/italic dim]")
        console.print()

        categories = [
            ("critical", "bold red",    "CRITICAL"),
            ("warnings", "bold yellow", "WARNINGS"),
            ("info",     "bold cyan",   "INFO"),
        ]
        any_found = False
        for key, style, label in categories:
            items = result.get(key, [])
            if not items:
                continue
            any_found = True
            console.print(f"[{style}]{label} ({len(items)})[/{style}]")
            for item in items:
                loc = item.get("line", "?")
                issue = item.get("issue", "")
                fix = item.get("fix", "")
                console.print(f"  [dim]@[/dim] [bold]{loc}[/bold]  {issue}")
                console.print(f"  [green]→[/green] [dim]{fix}[/dim]")
                console.print()
        if not any_found:
            console.print("[green]No issues found![/green]")


    @staticmethod
    def show_refactor(result: dict):
        score = result.get("score", {})
        if score:
            before = score.get("before", "?")
            after = score.get("after", "?")
            console.print(
                f"[bold]Quality score:[/bold]"
                f"[dim]{before}/10[/dim] → [bold green]{after}/10[/bold green]"
            )
        console.print(f"[italic dim]{result.get('summary', '')}[/italic dim]")
        console.print()

        categories = [
            ("readability", "cyan",   "READABILITY"),
            ("performance", "yellow", "PERFORMANCE"),
            ("style",       "blue",   "STYLE"),
        ]
        for key, color, label in categories:
            items = result.get(key, [])
            if not items:
                continue
            console.print(f"[bold {color}]{label}[/bold {color}]")
            for item in items:
                console.print(f"  • [bold]{item.get('what', '')}[/bold]")
                console.print(f"    [dim]{item.get('why', '')}[/dim]")
                example = item.get("example", "")
                if example:
                    syn = Syntax(example, "python", theme="monokai", line_numbers=False)
                    console.print("    ", syn)
                console.print()


    @staticmethod
    def show_tests(result: dict):
        framework = result.get("framework", "")
        notes = result.get("notes", "")
        coverage = result.get("coverage", [])
        tests = result.get("tests", "")

        console.print(f"[bold]Framework:[/bold] [bright_green]{framework}[/bright_green]")
        if notes:
            console.print(f"[dim]{notes}[/dim]")
        console.print()

        if tests:
            tests_clean = tests.replace("\\n", "\n")
            lang = "python" if "python" in framework.lower() or "pytest" in framework.lower() else "javascript"
            syn = Syntax(tests_clean, lang, theme="monokai", line_numbers=True)
            console.print(Panel(syn, title="[bold]Generated tests[/bold]", border_style="green"))

        if coverage:
            console.print()
            console.print("[bold]Coverage scenarios:[/bold]")
            for c in coverage:
                console.print(f" [green]✓[/green] {c}")


    @staticmethod
    def show_fixed_code(fixed: dict):

        summary = fixed.get("summary", "")
        code = fixed.get("fixed_code", "")

        console.print(summary)

        if code:
            console.print("\n[bold green]Fixed Code[/bold green]\n")
            console.print(code)

        changes = fixed.get("changes", [])

        if changes:
            console.print("\n[bold]Applied Changes[/bold]\n")

            for item in changes:
                console.print(
                    f"• {item.get('description', '')}"
                )


    @staticmethod
    def show_final_report(report: dict, log_path: str):
        console.print()
        console.print(Rule("[bold white]FINAL STRUCTURED REPORT[/bold white]", style="white"))

        table = Table(box=box.ROUNDED, show_header=True, header_style="bold white",
                      border_style="bright_blue", padding=(0, 2))
        table.add_column("Metric", style="dim", min_width=22)
        table.add_column("Result", style="bold white", min_width=20)

        critical = report.get("critical_bugs", 0)
        warnings = report.get("warnings", 0)

        table.add_row("Language", report.get("language", "-"))
        table.add_row("Complexity", report.get("complexity", "-"))
        table.add_row("Critical bugs", f"[bold red]{critical}[/bold red]" if critical else "[green]0[/green]")
        table.add_row("Warnings", f"[yellow]{warnings}[/yellow]" if warnings else "[green]0[/green]")
        table.add_row("Info notes", str(report.get("info_notes", 0)))
        table.add_row("Quality before", f"{report.get('quality_before', '?')}/10")
        table.add_row("Quality after", f"[bold green]{report.get('quality_after', '?')}/10[/bold green]")
        table.add_row("Code fixed", "Yes" if report.get("code_fixed") else "No")
        table.add_row("Test framework", report.get("test_framework", "-"))
        table.add_row("Test scenarios", str(report.get("test_scenarios", 0)))

        console.print(table)
        console.print()
        console.print(f"[dim]Run log saved →[/dim] [bold cyan]{log_path}[/bold cyan]")
        console.print()
