import json

import pytest

import config_manager


class TestConfigManager:

    @pytest.mark.asyncio
    async def test_init_(self):
        cm = config_manager.ConfigManager()
        assert cm

    @pytest.mark.asyncio
    async def test_get_config_data(self):
        cm = config_manager.ConfigManager(True)
        value = await cm.get_config_value('adsserver')
        assert isinstance(value, str)

    @pytest.mark.asyncio
    async def test_get_invalid_config_data(self):
        cm = config_manager.ConfigManager(True)
        with pytest.raises(ValueError):
            await cm.get_config_value('host')

    @pytest.mark.asyncio
    async def test_config_default_content(self):
        cm = config_manager.ConfigManager(True)
        value = await cm.get_config_value('commands')
        assert isinstance(value, list)

    @pytest.mark.asyncio
    async def test_get_config_data(self):
        cm = config_manager.ConfigManager(True)
        data = await cm.get_config_data()
        assert 'adsserver' in data
        assert 'port' in data

    @pytest.mark.asyncio
    async def test_save_config_entry(self):
        cm = config_manager.ConfigManager(True)
        await cm.save_entry('adsserver', '192.168.0.1')

        fp = cm.get_config_file_path()
        with open(fp) as json_file:
            data = json.load(json_file)

        assert 'adsserver' in data
        assert data['adsserver'] == '192.168.0.1'
