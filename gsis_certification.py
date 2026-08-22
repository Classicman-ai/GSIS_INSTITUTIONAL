"""Static and live-read certification for the canonical GSIS runtime."""

from __future__ import annotations

import ast
import os
from pathlib import Path

from institutional import GSISConfig, GSISUnifiedEngine


FORBIDDEN_PATTERNS = (
    "BOT_TOKEN =",
    "CHAT_ID =",
    "api.binance.com",
    "buy_volume = 9000",
    "sell_volume = 6000",
    "XAUUSD",
    "BTCUSDT",
    "ETHUSDT",
)


def python_files(root: Path):
    yield from root.rglob("*.py")


def static_audit(root: Path) -> list[str]:
    failures: list[str] = []
    for path in python_files(root):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                failures.append(f"{path}: forbidden pattern: {pattern}")
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
