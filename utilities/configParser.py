import json
import os

CONFIG_FILE_NAME = "config.json"


class ConfigParser(object):
    def __init__(self):
        super().__init__()

    def read_config_value(self, key):
        value = None
        try:
            with open(CONFIG_FILE_NAME, 'r') as f:
                config = json.load(f)
                value = config[key]
        except:
            print("Error reading value from config file")
        finally:
            return value

    def write_config_value(self, key, value):
        command = "a" if os.path.exists(CONFIG_FILE_NAME) else "w"
        try:
            with open(CONFIG_FILE_NAME, command) as f:
                data = {}
                data[key] = value
                json.dump(data, f)
            return True
        except:
            print("Error writing value to config file")
            return False
