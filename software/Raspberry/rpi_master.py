import sqlite3
#import smbus
from configparser import ConfigParser
import time
#import Adafruit_ADS1x15
from rpi_DB import Status, ClusterDB
from STM32 import STM32_addr, STM32_leds
from Grafana import Grafana

config = ConfigParser()
config.read('config.ini')
MAX_R = float(config.get('settings', 'MAX_R')) # KOm
MIN_R = float(config.get('settings', 'MIN_R')) # KOm
LUX_100 = MIN_R # Maximum brightness; needs to be calibrated
LUX_10 = MAX_R # Minimum brightness; needs to be calibrated
ADC_PIN = int(config.get('settings', 'ADC_PIN')) # GPIO4 on Rpi
CLUSTERS_NUM = int(config.get('settings', 'CLUSTERS_NUM'))

class STM32:
    def __init__(self, addr, name, leds) -> None:
        self.address = addr
        self.name = name
        self.leds_num = leds
    def addr(self):
        return self.address
    def name(self):
        return self.name
    def leds(self):
        return self.leds_num

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
        #self.adc = ADC(ADC_PIN)
        #self.bus = smbus.SMBus(1)
        self.stm32 = [None]*num_of_clusters
        self.db = ClusterDB()
        self.grafana = Grafana(self.db)
        self.clusters = ['oasis', 'illusion', 'mirage', 'atlantis', 'atrium']
        self.num_of_clusters = num_of_clusters
    def init_slaves(self):
        # init all STM32
        for stm32 in range(0, self.num_of_clusters):
            cluster_name = self.clusters[stm32]
            i2c_addr = STM32_addr.get(cluster_name)
            leds = STM32_leds.get(cluster_name)
            self.stm32[stm32] = STM32(i2c_addr, cluster_name, leds)

    def monitor_clusters(self):
        # parse metrics data for each cluster
        # ask bd if any changes per mac (try to change status)
        # based on return value construct msg to stm, at the end update stm32
        # self.grafana.get_metrics() # grafana class updates bd
        self.db.change_mac_status('oasis', 'a3', int(Status.EXAM))
        self.db.change_mac_status('oasis', 'a1', int(Status.USED))
        self.db.change_mac_status('oasis', 'a4', int(Status.EXAM))
        for cluster in self.clusters:
            # get number of leds in cluster
            # get value by led id
            print(cluster)
            self.construct_packet(cluster)
    def update_bd(self):
        pass
    def construct_packet(self, cluster):
        stm32 = self.clusters.index(cluster)
        leds = self.stm32[stm32].leds()
        i2c_array = [None] * (6 + leds)
        i2c_array[0] = Status.FREE
        i2c_array[1] = Status.USED
        i2c_array[2] = Status.COVID
        i2c_array[3] = Status.EXAM
        i2c_array[4] = 0 # WTF
        #i2c_array[5] = self.getBrightnessLevel()
        self.fill_cluster_array(cluster, i2c_array, leds)
        stm32_addr = self.stm32[stm32].addr()
        #self.send_packet(stm32_addr, i2c_array)
    def send_packet(self, addr, data):
        self.bus.write_i2c_block_data(addr, 0, data)
    def fill_cluster_array(self, cluster, data, leds):
        # import data from db one by one
        for led in range(0, leds):
            data[6+led] = self.db.fetch_cluster_led_status(cluster, led)
        print(data)
        # cluster_data = []
        # cluster_status = self.db.fetch_cluster_led_status(cluster, 3)
        # cluster_data = self.db.fetch_cluster_data(cluster, cluster_data)
        # print(cluster_status)
        # print(cluster_data)
        # self.db.change_mac_status(cluster, 'b2', 3)
        # cluster_status = self.db.fetch_cluster_led_status(cluster, 6)
        # print(cluster_status)

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
    rpi = Master(CLUSTERS_NUM)
    rpi.init_slaves()
    rpi.monitor_clusters()

