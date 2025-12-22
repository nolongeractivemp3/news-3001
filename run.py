import json
import os

config = json.load(open("config.json"))
os.system(f"sudo ./ui/frankenphp php-server -r ./ui/. -P {config['port']}")
