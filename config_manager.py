import os
import typing

import quart

CONFIG_FILE_PATH = os.path.abspath(os.path.join('', "config.json"))


class ConfigManager:

    def __init__(self, delete_act_config=False):
        config_file_path = self.get_config_file_path()
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

    async def get_config_data(self):
        config_file_path = self.get_config_file_path()
        with open(config_file_path) as config_file:
            return quart.json.load(config_file)

    async def get_config_value(self, key: str, default: str = None):
        data = await self.get_config_data()
        if key in data:
            return data[key]

        if default:
            return default

        raise ValueError('Key ' + key + ' not in config data')

    async def _write_config_file(self, config_data):
        config_file_path = self.get_config_file_path()
        with open(config_file_path, "w") as config_file:
            config_file.write(quart.json.dumps(config_data))
            config_file.flush()
            config_file.close()

    async def save_entry(self, key: str, value: typing.Union[str, list]):
        data = await self.get_config_data()
        data[key] = value
        await self._write_config_file(data)

    @staticmethod
    def get_config_file_path():
        return CONFIG_FILE_PATH
