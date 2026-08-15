import subprocess
import datetime
import sys


print("==============================")
print("GSIS MASTER ORCHESTRATOR v1.2")
print("==============================")

start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

print(f"START TIME: {start_time}")
print()


ENGINES = [

    # MARKET DATA
    "engines.market.live_price_connector",

    # INTELLIGENCE
    "engines.adapters.bayesian_adapter",
    "engines.adapters.regime_adapter",
    "engines.adapters.confirmation_adapter",
    "engines.adapters.qualification_adapter",

    # AUTHORITY
    "engines.authority.authority_engine",
    "engines.fusion.fusion_bridge",

    # CAPITAL PROTECTION
    "engines.risk.risk_guard_engine",

    # EXECUTION
    "engines.execution.execution_gate",

    # POSITION CONTROL
    "engines.management.position_manager",

    # MONITORING
    "engines.monitor.price_monitor",

    # EVENTS
    "engines.events.trade_event_engine",

    # PERFORMANCE
    "engines.performance.profit_calculation_engine",
    "engines.performance.equity_update_engine",
    "engines.performance.performance_analytics_engine",

    # REPORTING
    "engines.reporting.report_integration_engine"

]


for engine in ENGINES:

    print("------------------------------")
    print(f"RUNNING: {engine}")
    print("------------------------------")

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                engine
            ],
            text=True
        )


        if result.returncode != 0:

            print()
            print("ENGINE FAILED:")
            print(engine)
            print("STOPPING MASTER CYCLE")
            break


    except Exception as error:

        print()
        print("MASTER ERROR:")
        print(error)
        break



print()
print("==============================")
print("GSIS MASTER CYCLE COMPLETE")
print("==============================")
print("STATUS: OPERATIONAL 🛡️")
