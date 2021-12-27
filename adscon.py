import pyads


class AdsConnector:

    def __init__(self):
        self._plc = None
        self._actServer = None
        self._actAMsId = None
        self._actPort = None
        pyads.open_port()

    def initialize(self, server_address, server_amsnetid, port):
        if pyads.utils.platform_is_linux():
            adr = pyads.AmsAddr(server_amsnetid, int(port))
            pyads.add_route(adr, server_address)

        self._plc = pyads.Connection(server_amsnetid, int(port))
        self._actServer = server_address
        self._actAMsId = server_amsnetid
        self._actPort = port

    def _re_initialize(self):
        if self._actPort:
            self.initialize(self._actServer, self._actAMsId, self._actPort)
        else:
            raise ValueError("No valid configuration for ADS Server Available")

    def check_connection(self):
        successful = False
        ip = self._actPort
        counter = 0
        while not successful and counter < 5:
            self._plc.open()
            try:
                ip = self._plc.read_device_info()
                successful = True
            except pyads.pyads_ex.ADSError as adsError:
                self._re_initialize()
                counter += 1
                if counter >= 5:
                    raise adsError
            self._plc.close()

        return ip

    @staticmethod
    def _parse_ads_type(ads_type_as_string):
        convert_values = {
            'PLCTYPE_INT': pyads.PLCTYPE_INT,
            'PLCTYPE_WORD': pyads.PLCTYPE_WORD,
            'PLCTYPE_DWORD': pyads.PLCTYPE_DWORD,
            'PLCTYPE_REAL': pyads.PLCTYPE_REAL
        }
        if ads_type_as_string in convert_values:
            return convert_values[ads_type_as_string]

        raise ValueError("Invalid ads type: " + ads_type_as_string)

    def send_ads_read_command(self, ads_index_group: str, ads_index_offset: str, ads_type: str):
        if not self._plc:
            raise pyads.ADSError("No connection initialized")

        self._plc.open()
        value = self._plc.read(int(ads_index_group, 0), int(ads_index_offset, 0), self._parse_ads_type(ads_type))
        self._plc.close()

        return value

    @staticmethod
    def _parse_data(ads_type, data):
        if ads_type == pyads.PLCTYPE_REAL:
            return float(data)
        return int(data, 0)

    def send_ads_write_command(self, ads_index_group: str, ads_index_offset: str, ads_type: str, data):
        if not self._plc:
            raise pyads.ADSError("No connection initialized")

        ads_type = self._parse_ads_type(ads_type)

        self._plc.open()
        self._plc.write(int(ads_index_group, 0), int(ads_index_offset, 0), self._parse_data(type, data), ads_type)
        self._plc.close()

        return True
