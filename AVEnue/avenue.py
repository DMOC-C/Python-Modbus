####################################
# 
# AVEnue (Analog Value Emulator)
# 
# (C) 2019 CACI, Inc.
#
# POC:  Scott Thompson
# scott.thompson@caci.com
# 832-570-5758
#
####################################

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from time import sleep
from random import randint, seed

#
# Setup Global Variables
#
target = '192.168.107.12'
freq = 0.0
speed = 0
poles = 4
volts = 0
amps = 0
pf = 0.8
kva = 0.0
kw = 0.0


def check_gen():
    #
    # Opens up a Modbus Connection with the PLC and
    # checks coil at address 2 for a TRUE value.
    # When that occurs, pushes control to the
    # start_gen() function.
    #
    client = ModbusClient(target)
    while True:
        result = client.read_coils(2, 1)
        if result.bits[0]:
            start_gen()


def start_gen():
    global speed
    global volts
    global freq
    #
    # Start Geneator
    # 0 to 1800 RPM in 3 seconds
    # broken into 100 millisecond segments
    #
    sleep(5)
    client = ModbusClient(target)
    for x in range(1, 31):
        speed = speed + 60
        freq = (speed * poles) / 120
        print(freq)
        y = int(freq)
        client.write_register(1, y)
        print(speed)
        client.write_register(0, speed)
        sleep(.1)
    #
    # Voltage Regulator begin excitation
    # 0 to 440 Volts in 2 seconds
    # Broken into 100 millisecond segments
    #
    for x in range(1, 21):
        volts = volts + 22
        print(volts)
        client.write_register(2, volts)
        sleep(.1)
    #
    # After generator comes up to speed and voltage,
    # breaker is shut (Coil address 3) and control
    # is given to run_gen() function.
    #
    client.write_coil(3, True)
    run_gen()


def run_gen():
    global amps
    seed(1)
    client = ModbusClient(target)
    #
    # Choose random integers between 1700 and
    # 1750 to show changes in generator load.
    # Recompute KVA and KW.  Push values to
    # the PLC.
    #
    while True:
        amps = randint(1700, 1750)
        client.write_register(3, amps)
        kva = ((1.732) * amps * volts) / 1000
        client.write_register(4, int(kva))
        kw = pf * kva
        client.write_register(5, int(kw))
        sleep(1)


check_gen()
