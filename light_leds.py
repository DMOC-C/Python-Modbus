from pymodbus.client.sync import ModbusTcpClient

pi = ModbusTcpClient("localhost", 5020)
pi.write_coil(0, 1)
