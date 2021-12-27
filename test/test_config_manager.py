import pytest

import config_manager


@pytest.mark.asyncio
async def test_get_config_data():
    await config_manager.init_config_file(True)
    value = await config_manager.get_config_value('adsserver')
    assert isinstance(value, str)


@pytest.mark.asyncio
async def test_get_invalid_config_data():
    await config_manager.init_config_file(True)
    with pytest.raises(ValueError):
        await config_manager.get_config_value('host')


@pytest.mark.asyncio
async def test_config_default_content():
    await config_manager.init_config_file(True)
    value = await config_manager.get_config_value('commands')
    assert isinstance(value, dict)


@pytest.mark.asyncio
async def test_get_config_data():
    await config_manager.init_config_file(True)
    data = await config_manager.get_config_data()
    assert 'adsserver' in data
    assert 'port' in data
