"""
Multi-Agent Code Review Pipeline
Usage:
    python main.py                          # interactive prompt
    python main.py --file path/to/code.py   # review a file
    python main.py --demo                   # run with built-in sample
"""

import argparse
import sys
from pathlib import Path

from pipeline import CodeReviewPipeline
from ui import UI


SAMPLE_CODE = '''\
def fetch_user_data(user_id):
    url = "https://api.example.com/users/" + user_id
    import requests
    response = requests.get(url)
    data = response.json()
    print("<b>" + data["name"] + "</b>")   # XSS risk in web context
    return data

def calculate_discount(price, discount_percent):
    discount = price / 100 * discount_percent
    return price - discount

def process_orders(orders):
    total = 0
    for i in range(len(orders) + 1):       # off-by-one: IndexError on last iteration
        total += orders[i]["price"] * orders[i]["quantity"]
    return total

def find_user(users, name):
    for user in users:
        if user["name"] == name:
            return user
    # returns None implicitly — callers never check
'''


def get_code(args) -> str:
    if args.demo:
        return SAMPLE_CODE
    if args.file:
        path = Path(args.file)
        if not path.exists():
            UI.error(f"File not found: {args.file}")
            sys.exit(1)
        return path.read_text()
    # interactive
    UI.banner()
    UI.print("\n[bold]Paste your code below.[/bold] When done, enter a line with only [cyan]END[/cyan] and press Enter.\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    code = "\n".join(lines).strip()
    if not code:
        UI.error("No code provided.")
        sys.exit(1)
    return code


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Code Review Pipeline")
    parser.add_argument("--file", help="Path to source file to review")
    parser.add_argument("--demo", action="store_true", help="Run with built-in sample code")
    parser.add_argument("--no-color", action="store_true", help="Disable rich formatting")
    args = parser.parse_args()

    if not args.demo and not args.file:
        UI.banner()

    code = get_code(args)

    pipeline = CodeReviewPipeline()
    pipeline.run(code)


main()
