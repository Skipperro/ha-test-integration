import unittest
import custom_components.ha_test_integration.sensor as sensor

class IPSensorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ipv4 = sensor.IPSensor(False)
        self.ipv6 = sensor.IPSensor(True)

    def validate_ipv4(self, s: str):
        # IPv4 address is a string of 4 numbers separated by dots
        a = s.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    async def test_update_ipv4(self):
        await self.ipv4.async_update()
        assert self.validate_ipv4(self.ipv4.native_value)

    async def test_update_ipv6(self):
        await self.ipv6.async_update()
        assert len(self.ipv6.native_value) > 5
        isv4 = self.validate_ipv4(self.ipv6.native_value)
        if not isv4:
            s = self.ipv6.native_value.split(':')
            assert len(s) > 4
