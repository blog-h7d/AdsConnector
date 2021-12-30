# pylint: disable=W0212
# pylint: disable=W0613
# pylint: disable=W0621
# pylint: disable=W0622
import os

import pytest

import adscon
import config_manager
import controller


@pytest.fixture(name='test_app')
def _test_app():
    return controller.app.test_app().test_client()


def mock_get_file_path(obj=None):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))


@pytest.mark.asyncio
async def test_save_commands_simple(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    result = await test_app.post('/command/save/')
    assert result.status_code == 302


@pytest.mark.asyncio
async def test_save_commands_data(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    data = {
        '0-ID': 'id100',
        '0-Command': 'command',
        '0-Group': 'command',
        '0-Type': 'PLCTYPE_INT',
    }
    result = await test_app.post('/command/save/', form=data)
    assert result.status_code == 302

    saved_data = await adscon.page.config.get_config_value('commands')
    assert saved_data


@pytest.mark.asyncio
async def test_save_commands_invalid(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    result = await test_app.get('/command/save/')
    assert result.status_code == 405


@pytest.mark.asyncio
async def test_check_command(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('commands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': '',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_read(*args, **kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_read_command', mock_send_read)

    result = await test_app.get('/command/check/1234/')

    assert result.status_code == 200
    assert called
