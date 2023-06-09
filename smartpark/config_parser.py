import json

def parse_config(path: str) -> dict:
    """Parse the config file and return the values as a dictionary"""
    with open(path, 'r') as config:
        return json.load(config)