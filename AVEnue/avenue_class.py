"""
AVEnue (Analog Value Emulator)

(C) 2019 CACI Intl.

POC: Scott Thompson
scott.thompson@caci.com
832-570-5758
"""
from pymodbus.client.sync import ModbusTcpClient as ModClient
from random import randint, seed
from time import sleep


class Generator:
    """Simulates an electrical generator, with variance in output voltage."""
    def __init__(self, gen_ip_add="192.168.107.12", freq=0.0, speed=0, poles=4, volts=0, amps=0, pf=0.8, kva=0.0,
                 kw=0.0):
        self.client = ModClient(gen_ip_add)
        self.freq = float(freq)
        self.speed = int(speed)
        self.poles = int(poles)
        self.volts = float(volts)
        self.amps = float(amps)
        self.power_factor = float(pf)
        self.kva = float(kva)
        self.kw = float(kw)

    def check_gen(self):
        """Open connection w/ PLC. If coil 2 is True, call start_gen() method."""
        while True:
            result = self.client.read_coils(2, 1)
            if result.bits[0]:
                self.start_gen()

    def start_gen(self):
        """Simulates generator startup procedure.

        At initial startup, it takes 3 seconds for generator to get up to speed (1800 rpm). This is divided into 100
        millisecond segments.

        Next, the voltage regulator is excited, increasing from 0V to 440V in 2 seconds, broken into 100 ms segments.

        Finally, when the generator is in steady-state condition of normal speed and voltage, the breaker (coil 3) is
        shut and control passed to the run_gen() method.
        """
        sleep(5)

        # Bring generator up to speed
        for i in range(1, 31):
            self.speed = self.speed + 60
            self.freq = (self.speed * self.poles) / 120
            print(f"Generator frequency: {self.freq}Hz")
            self.client.write_register(1, int(self.freq))
            print(f"Generator speed: {self.speed} rpm")
            self.client.write_register(0, self.speed)
            sleep(0.1)

        # Bring up voltage
        for i in range(1, 21):
            self.volts = self.volts + 22
            print(f"Generator voltage: {self.volts}V")
            self.client.write_register(2, self.volts)
            sleep(0.1)

        # Shut breaker and move to run conditions
        self.client.write_coil(3, True)
        self.run_gen()

    def run_gen(self):
        """Randomly generate output values, within a set range, to simulate true power fluctuations."""
        seed(1)
        while True:
            self.amps = randint(1700, 1750)
            self.client.write_register(3, self.amps)

            self.kva = (1.732 * self.amps * self.volts) / 1000
            self.client.write_register(4, int(self.kva))

            self.kw = self.power_factor * self.kva
            self.client.write_register(5, int(self.kw))

            sleep(1)


if __name__ == "__main__":
    generator = Generator()
    generator.check_gen()
