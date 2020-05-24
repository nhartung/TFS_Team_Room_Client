import json

class Missing_Required_Configuration_Value(Exception):
    pass

config_data = None

def load_configuration():
    global config_data
    config_data = json.load(open('./tfs_config.json'))
    if _invalid_configuration():
        raise Missing_Required_Configuration_Value()

def _invalid_configuration():
    global config_data
    if _check_empty('domain'):
        return True
    if _check_empty('base_url'):
        return True
    return False

def _check_empty(key):
    global config_data
    if key not in config_data or config_data[key] == '':
        return True

def get_domain():
    if not config_data:
        load_configuration()
    return config_data['domain']

def get_base_url():
    if not config_data:
        load_configuration()
    return config_data['base_url']
