import json

config_data = None

def load_configuration():
    global config_data
    config_data = json.load(open('./tfs_chatclient/tfs_config.json'))

def get_domain():
    if not config_data:
        load_configuration()
    return config_data['domain']

def get_base_url():
    if not config_data:
        load_configuration()
    return config_data['base_url']
