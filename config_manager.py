import os

import quart

CONFIG_FILE_PATH = os.path.abspath(os.path.join('', "config.json"))


async def init_config_file(delete_act_config=False):
    config_file_path = await get_config_file_path()
    if not os.path.exists(config_file_path) or delete_act_config:
        if os.path.exists(config_file_path):
            os.remove(config_file_path)

        with open(config_file_path, "w") as config_file:
            default_data = {
                "adsserver": "",
                "amsnetid": "",
                "port": "851",
                "commands": list(),
                "writecommands": list()
            }
            config_file.write(quart.json.dumps(default_data))


async def get_config_data(configfile: str = ""):
    await init_config_file()

    config_file_path = await get_config_file_path()
    with open(config_file_path) as config_file:
        text = config_file.read()
        json_obj = quart.json.loads(text)
        return json_obj


async def get_config_value(key: str, default: str = None):
    data = await get_config_data()
    if key in data:
        return data[key]

    if default:
        return default

    raise ValueError('Key ' + key + ' not in config data')


async def write_config_file(config_data):
    config_file_path = await get_config_file_path()
    with open(config_file_path, "w") as config_file:
        config_file.write(quart.json.dumps(config_data))
        config_file.flush()
        config_file.close()


async def get_config_file_path():
    return CONFIG_FILE_PATH
