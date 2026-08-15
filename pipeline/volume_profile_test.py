from engines.volume_profile_engine import VolumeProfileEngine


print("===================================")
print("GSIS ENGINE 8.2 TEST")
print("VOLUME PROFILE INTELLIGENCE")
print("===================================")


engine = VolumeProfileEngine()

engine.start()


result = engine.calculate(
    "BTCUSDT",
    "M15"
)


print(result)


print("-----------------------------------")
print("VOLUME PROFILE COMPLETE")
