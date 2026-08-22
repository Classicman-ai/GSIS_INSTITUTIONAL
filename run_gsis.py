"""Canonical GSIS Institutional entry point."""

from institutional import GSISConfig, GSISUnifiedEngine


def main() -> None:
    config = GSISConfig.from_env()
    engine = GSISUnifiedEngine(config)
    engine.run_forever()


if __name__ == "__main__":
    main()
