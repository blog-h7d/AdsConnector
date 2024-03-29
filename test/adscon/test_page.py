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
    print(os.path.dirname(__file__))
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


@pytest.mark.asyncio
async def test_check_command_default(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('commands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '1234',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_read(_, command, group, return_type):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '1234'

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_read_command', mock_send_read)

    result = await test_app.get('/command/check/1234/')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_command(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('commands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': '123',
        'default': '5678',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_read(_, command, group, return_type):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '123'

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_read_command', mock_send_read)

    result = await test_app.get('/command/run/1234/')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_command_default(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('commands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '5678',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_read(_, command, group, return_type):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '345'

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_read_command', mock_send_read)

    result = await test_app.get('/command/run/1234/?groups=345')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_command_defaults(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('commands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '5678',
        'type': 'PLCTYPE_INT'
    }])

    called = 0

    def mock_send_read(_, command, group, return_type):
        nonlocal called
        called += 1
        assert command == '0x80000001'
        assert group in ('345', '346', '347')

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_read_command', mock_send_read)

    result = await test_app.get('/command/run/1234/?groups=345,346,347')

    assert result.status_code == 200
    assert called == 3


@pytest.mark.asyncio
async def test_save_exec_commands_simple(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    result = await test_app.post('/command/exec/save/')
    assert result.status_code == 302


@pytest.mark.asyncio
async def test_save_exec_commands_data(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    data = {
        '0-ID': 'id100',
        '0-Command': 'command',
        '0-Group': 'command',
        '0-Type': 'PLCTYPE_INT',
        '0-DefaultValue': 'value'
    }
    result = await test_app.post('/command/exec/save/', form=data)
    assert result.status_code == 302

    saved_data = await adscon.page.config.get_config_value('writecommands')
    assert saved_data


@pytest.mark.asyncio
async def test_check_exec_command(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('writecommands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': '',
        'type': 'PLCTYPE_INT',
        'defaultValue': 1
    }])

    called = False

    def mock_send_write(*args, **kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_write_command', mock_send_write)

    result = await test_app.get('/command/exec/check/1234/')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_check_exec_command_default(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('writecommands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '123',
        'type': 'PLCTYPE_INT',
        'defaultValue': 1
    }])

    called = False

    def mock_send_write(_, command, group, value_type, value):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '123'
        assert value_type == 'PLCTYPE_INT'
        assert value == 1

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_write_command', mock_send_write)

    result = await test_app.get('/command/exec/check/1234/')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_exec_command(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('writecommands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': '123',
        'default': '5678',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_write(_, command, group, value_type, value):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '123'
        assert value == '1'

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_write_command', mock_send_write)

    result = await test_app.get('/command/exec/run/1234/1/')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_exec_command_default(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('writecommands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '5678',
        'type': 'PLCTYPE_INT'
    }])

    called = False

    def mock_send_write(_, command, group, value_type, value):
        nonlocal called
        called = True
        assert command == '0x80000001'
        assert group == '345'
        assert value == 'abc'

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_write_command', mock_send_write)

    result = await test_app.get('/command/exec/run/1234/abc/?groups=345')

    assert result.status_code == 200
    assert called


@pytest.mark.asyncio
async def test_run_exec_command_defaults(test_app, monkeypatch):
    monkeypatch.setattr(config_manager.ConfigManager, 'get_config_file_path', mock_get_file_path)
    controller.config = config_manager.ConfigManager()

    await controller.config.save_entry('writecommands', [{
        'identifier': '1234',
        'command': '0x80000001',
        'group': 'default',
        'default': '5678',
        'type': 'PLCTYPE_REAL'
    }])

    called = 0

    def mock_send_write(_, command, group, value_type, value):
        nonlocal called
        called += 1
        assert command == '0x80000001'
        assert group in ('345', '346', '347')
        assert value_type == 'PLCTYPE_REAL'
        assert value == "1.0"

    monkeypatch.setattr(adscon.connector.AdsConnector, 'send_ads_write_command', mock_send_write)

    result = await test_app.get('/command/exec/run/1234/1.0/?groups=345,346,347')

    assert result.status_code == 200
    assert called == 3
