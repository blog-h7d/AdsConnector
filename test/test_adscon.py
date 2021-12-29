import pyads
import pytest

import adscon


def get_server_ip():
    return '192.168.178.254'


def test_pyads_installed_correctly():
    plc = pyads.Connection(get_server_ip() + ".1.1", 851)
    pyads.open_port()


def test_check_connection():
    server_ip = get_server_ip()
    connector = adscon.AdsConnector()
    connector.initialize(server_ip, server_ip + ".1.1", 851)
    assert connector.check_connection(), "Failed to connect to AMSNetId: " + server_ip + ".1.1"


def test_check_no_connection():
    server_ip = "192.168.47.3"  # invalid ip should be used
    connector = adscon.AdsConnector()
    connector.initialize(server_ip, server_ip + ".1.1", 851)
    with pytest.raises(pyads.pyads_ex.ADSError):
        connector.check_connection()


@pytest.mark.parametrize("type_as_string, expected_value", [
    ("PLCTYPE_INT", pyads.PLCTYPE_INT),
])
def test_parse_ads_type(type_as_string, expected_value):
    assert adscon.AdsConnector._parse_ads_type(type_as_string) == expected_value


@pytest.mark.parametrize("type_as_string", ["", "abc", "PLCTYPE"])
def test_parse_invalid_ads_type(type_as_string):
    with pytest.raises(ValueError):
        adscon.AdsConnector._parse_ads_type(type_as_string)


class DummyPlc:

    def open(self):
        return True

    def close(self):
        return True

    def read(self, command, idxgrp, type):
        return int(command) + int(idxgrp)

    def write(self, command, idxgrp, data, type):
        return int(command) + int(idxgrp)


@pytest.fixture
def dummy_plc():
    plc = DummyPlc()

    yield plc


def test_send_ads_read_command(dummy_plc):
    connector = adscon.AdsConnector()
    connector._plc = dummy_plc
    assert connector.send_ads_read_command("8000", "1", "PLCTYPE_INT") == 8001


def test_send_ads_read_noplc():
    connector = adscon.AdsConnector()
    with pytest.raises(pyads.ADSError):
        connector.send_ads_read_command("8000", "1", "PLCTYPE_INT")


def test_send_ads_write_command(dummy_plc):
    connector = adscon.AdsConnector()
    connector._plc = dummy_plc
    assert connector.send_ads_write_command("8000", "1", "PLCTYPE_INT", "1")
