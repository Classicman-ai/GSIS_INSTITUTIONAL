"""
=========================================================
GSIS INSTITUTIONAL
Configuration Manager
Version: 1.0
=========================================================
"""

import json
import os


class ConfigManager:

    def __init__(self, config_file="config/config.json"):
        self.config_file = config_file
        self.config = {}

    def load(self):

        if not os.path.exists(self.config_file):
            print(f"[CONFIG] File not found: {self.config_file}")
            return False

        with open(self.config_file, "r") as f:
            self.config = json.load(f)

        print("[CONFIG] Configuration loaded successfully.")
        return True

    def save(self):

        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

        print("[CONFIG] Configuration saved.")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def exists(self, key):
        return key in self.config

    def show(self):

        print("\n========== CONFIGURATION ==========")

        if not self.config:
            print("No configuration loaded.")
            return

        for key, value in self.config.items():
            print(f"{key}: {value}")
