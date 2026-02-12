#!/usr/bin/env python3
"""Simple fixer for gosec-produced SARIF files.

Gosec emits SARIF where some `rules[].relationships` entries are not objects
which makes the SARIF invalid for GitHub's `upload-sarif` action. This script
removes the `relationships` property from any rule where one or more items are
not objects. It's conservative and only touches the SARIF when needed.
"""
import json
import sys
from pathlib import Path


def fix(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read/parse {path}: {e}")
        return 2

    changed = False
    runs = data.get("runs") or []
    for run in runs:
        tool = run.get("tool", {})
        driver = tool.get("driver", {})
        rules = driver.get("rules") or []
        for r in rules:
            if "relationships" in r:
                rel = r.get("relationships")
                if isinstance(rel, list):
                    # If any element is not a dict, drop the relationships key
                    if any(not isinstance(elem, dict) for elem in rel):
                        print(
                            "Removing invalid 'relationships' from rule:",
                            r.get("id") or r.get("name") or "<unknown>",
                        )
                        del r["relationships"]
                        changed = True

    if changed:
        try:
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            print(f"Failed to write fixed SARIF: {e}")
            return 3
        print(f"Fixed SARIF written to {path}")
    else:
        print("No changes required")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fix_gosec_sarif.py <sarif-file>")
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"SARIF file not found: {path}")
        sys.exit(2)
    sys.exit(fix(path))
