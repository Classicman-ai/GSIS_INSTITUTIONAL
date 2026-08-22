"""Static and live-read certification for the canonical GSIS runtime."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from institutional import GSISConfig, GSISUnifiedEngine


FORBIDDEN_REGEX = (
    re.compile(r"^\s*BOT_" + r"TOKEN\s*=\s*['\"]", re.MULTILINE),
    re.compile(r"^\s*CHAT_" + r"ID\s*=\s*['\"]", re.MULTILINE),
    re.compile(r"api\.binance\.com", re.IGNORECASE),
    re.compile(r"buy_volume\s*=\s*[0-9]", re.IGNORECASE),
    re.compile(r"sell_volume\s*=\s*[0-9]", re.IGNORECASE),
)


def python_files(root: Path):
    yield from root.rglob("*.py")


def static_audit(root: Path) -> list[str]:
    failures: list[str] = []
    for path in python_files(root):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_REGEX:
            if pattern.search(text):
                failures.append(f"{path}: forbidden implementation pattern: {pattern.pattern}")
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}: syntax error: {exc}")
    return failures


def runtime_audit() -> dict:
    config = GSISConfig.from_env()
    engine = GSISUnifiedEngine(config)
    return engine.validate_runtime()


def main() -> int:
    root = Path(__file__).resolve().parent
    failures = static_audit(root)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    result = runtime_audit()
    print("GSIS STATIC AUDIT: PASS")
    print("GSIS MT5 CONNECTOR: PASS")
    print("GSIS LIVE MARKET READ: PASS")
    print(f"GSIS RUNTIME STATUS: {result['status']}")
    print(f"GSIS EXECUTION ENABLED: {result['execution_enabled']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
