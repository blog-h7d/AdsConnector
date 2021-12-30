# pylint: disable=W0212
# pylint: disable=W0613
# pylint: disable=W0621
# pylint: disable=W0622

import pyads
import pytest

import adscon.connector


def get_server_ip():
    return '192.168.0.1'


def mock_add_route(*args):
    pass


class MockConnection:
    def __init__(self, amsnet_id, port):
        pass

    def open(self):
        return True

    def close(self):
        return True

    def read_device_info(self):
        return 'Successful'

    def read(self, command, idxgrp, type):
        return int(command) + int(idxgrp)

    def write(self, command, idxgrp, data, type):
        return int(command) + int(idxgrp)


def test_pyads_installed_correctly():
    pyads.Connection(get_server_ip() + ".1.1", 851)
    assert pyads.open_port()


def test_check_connection(monkeypatch):
    server_ip = get_server_ip()

    monkeypatch.setattr(pyads, "Connection", MockConnection)
    monkeypatch.setattr(pyads, "add_route", mock_add_route)

    connector = adscon.connector.AdsConnector()
    connector.initialize(server_ip, server_ip + ".1.1", 851)
    assert connector.check_connection(), "Failed to connect to AMSNetId: " + server_ip + ".1.1"


def test_check_no_connection(monkeypatch):
    monkeypatch.setattr(pyads, "add_route", mock_add_route)

    server_ip = "192.168.47.3"  # invalid ip should be used
    connector = adscon.connector.AdsConnector()
    connector.initialize(server_ip, server_ip + ".1.1", 851)
    with pytest.raises(pyads.pyads_ex.ADSError):
        connector.check_connection()


@pytest.mark.parametrize("type_as_string, expected_value", [
    ("PLCTYPE_INT", pyads.PLCTYPE_INT),
])
def test_parse_ads_type(type_as_string, expected_value):
    assert adscon.connector.AdsConnector._parse_ads_type(type_as_string) == expected_value


@pytest.mark.parametrize("type_as_string", ["", "abc", "PLCTYPE"])
def test_parse_invalid_ads_type(type_as_string):
    with pytest.raises(ValueError):
        adscon.connector.AdsConnector._parse_ads_type(type_as_string)


@pytest.fixture
def dummy_plc():
    plc = MockConnection("127.0.0.1.1.1", 851)

    yield plc


def test_send_ads_read_command(dummy_plc):
    connector = adscon.connector.AdsConnector()
    connector._plc = dummy_plc
    assert connector.send_ads_read_command("8000", "1", "PLCTYPE_INT") == 8001


def test_send_ads_read_noplc():
    connector = adscon.connector.AdsConnector()
    with pytest.raises(pyads.ADSError):
        connector.send_ads_read_command("8000", "1", "PLCTYPE_INT")


def test_send_ads_write_command(dummy_plc):
    connector = adscon.connector.AdsConnector()
    connector._plc = dummy_plc
    assert connector.send_ads_write_command("8000", "1", "PLCTYPE_INT", "1")
