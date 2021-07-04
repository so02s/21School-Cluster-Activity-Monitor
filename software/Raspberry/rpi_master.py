import sqlite3
import smbus
import time
import Adafruit_ADS1x15
from rpi_DB import Status, ClusterDB

MAX_R = 25 # KOm
MIN_R = 0.4 # KOm
LUX_100 = MIN_R # Maximum brightness; needs to be calibrated
LUX_10 = MAX_R # Minimum brightness; needs to be calibrated

class STM32:
    def __init__(self, addr) -> None:
        self.address = addr

class ADC:
    def __init__(self, pin) -> None:
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        self.pin = pin
    def read_pin(self, pin):
        return self.adc.read_adc(pin, gain=self.GAIN)
    def adc_test(self):
    # Read all the ADC channel values in a list.
        values = [0]*4
        for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
            values[i] = self.read_pin(i)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
            time.sleep(0.5)

class Master:
    def __init__(self, num_of_clusters) -> None:
        self.adc = ADC()
        self.bus = smbus.SMBus(1)
        self.stm32 = [num_of_clusters]
        self.db = ClusterDB()
        self.clusters = ['oasis', 'illusion', 'mirage', 'atlantis']
    def init_slaves(self):
        # init all STM32
        pass
    def monitor_clusters(self):
        # parse metrics data for each cluster
        # ask bd if any changes per mac (try to change status)
        # based on return value construct msg to stm, at the end update stm32
        for cluster in self.clusters:
            pass
    def update_bd(self):
        pass
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    def getBrightnessLevel(self):
        lvl = self.adc.read_pin(self.adc.pin)
        # lux level processing here
        return lvl
    def setBrightness(self, lvl, address):
        # implement protocol here
        self.writeByte(address, lvl)
    def setBrightnessAll(self):
        lux = self.getBrightnessLevel()
        for stm in self.stm32:
            self.setBrightness(stm.address, lux)




if __name__ == '__main__':
    rpi = Master(5)

