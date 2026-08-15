from system_info import *

print("=" * 50)
print("QMOS STATUS")
print("=" * 50)

print(f"System : {SYSTEM_NAME}")
print(f"Version: {SYSTEM_VERSION}")
print(f"Build  : {BUILD}")
print(f"Database Version: {DATABASE_VERSION}")

print("\nAssets:")
for asset in ASSETS:
    print(" -", asset)

print("\nTimeframes:")
for tf in TIMEFRAMES:
    print(" -", tf)

print("\nInstalled Engines:")
for key, value in ENGINES.items():
    print(f"{key}: {value}")

print("\nSystem Ready.")
