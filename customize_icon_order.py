#!/usr/bin/env python3
"""Interactive tool to customize rEFInd icon order.

This script updates the order of items in the `scanfor` and `showtools`
directives of a refind.conf file. Run the script and follow the prompts
to reorder these options.
"""

import argparse
import re
from typing import List


def parse_directive(line: str) -> List[str]:
    """Extract comma-separated tokens from a directive line."""
    # remove inline comments that appear after the options
    line = line.split('#', 1)[0]
    parts = line.split(None, 1)
    if len(parts) < 2:
        return []
    return [item.strip() for item in parts[1].split(',') if item.strip()]


def format_directive(name: str, items: List[str]) -> str:
    """Create a configuration line from directive name and tokens."""
    return f"{name} {','.join(items)}\n"


def reorder(items: List[str]) -> List[str]:
    """Interactively reorder items."""
    print("Current order:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    prompt = (
        "Enter new order as space-separated numbers (e.g. '3 1 2') or press "
        "Enter to keep current order: "
    )
    response = input(prompt).strip()
    if not response:
        return items
    try:
        indices = [int(x) - 1 for x in response.split()]
        if sorted(indices) != list(range(len(items))):
            raise ValueError
    except ValueError:
        print("Invalid input; keeping existing order.")
        return items
    return [items[i] for i in indices]


def process_file(path: str) -> None:
    """Read, modify, and write the configuration file."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    directive_pattern = re.compile(r'^(scanfor|showtools)\b', re.IGNORECASE)
    updated_lines = []
    for line in lines:
        match = directive_pattern.match(line.lstrip('#').lstrip())
        if match:
            name = match.group(1)
            items = parse_directive(line.lstrip('#').lstrip())
            if items:
                items = reorder(items)
                line = format_directive(name, items)
        updated_lines.append(line)

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Customize rEFInd icon order by editing refind.conf"
    )
    parser.add_argument(
        'conf_path',
        default='refind.conf',
        nargs='?',
        help='Path to refind.conf (default: refind.conf in current directory)',
    )
    args = parser.parse_args()
    process_file(args.conf_path)


if __name__ == '__main__':
    main()
