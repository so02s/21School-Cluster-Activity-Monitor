# Крч, переписывание кода, ваууу
import time
from STM32 import STM32_addr, STM32_leds, STM32_rooms
from smbus2 import SMBus, i2c_msg
# from utils.Grafana import Grafana
from utils.settings import STM32_command, clusters_conf, colors
from utils.colors import extract_color


 
class STM32:
    def __init__(self, addr, name, leds, rooms) -> None:
        self.address: int = addr
        self.name: str = name
        self.leds_num: int = leds
        self.rooms_num: int = rooms
    def addr(self) -> int:
        return self.address
    def name(self) -> str:
        return self.name
    def leds(self) -> int:
        return self.leds_num
    def rooms(self) -> int:
        return self.rooms_num
    


class Master:
    def __init__(self, clusters: list) -> None:
        self.clusters = clusters
        self.num_of_clusters = len(clusters)

        # бд для хранения мест (кто где сидит, что происходит)
        # self.db = ClusterDB()
        # slaves
        self.stm32: list[STM32] = [None]*self.num_of_clusters
        # для шины i2c
        self.bus = SMBus(1)
        # общение с API кластеров
        # self.grafana = Grafana(self.db)

        

        # ADC - АЦП, необходимый для работы фоторезистра. Светодиоды слишком яркие (даже на минимальной яркости)
        # из-за чего отказались от изменения яркости. Но в следующих версиях можно использовать часть кода, расположеную в utils/ADC
        # self.adc = ADC(ADC_PIN)

    # инициализвация всех STM32 - в каждом модуле по 1
    def init_slaves(self) -> None:
        for i, cluster in enumerate(self.clusters):
            i2c_addr = getattr(STM32_addr, cluster)
            leds = getattr(STM32_leds, cluster)
            rooms = getattr(STM32_rooms, cluster)
            self.stm32[i] = STM32(i2c_addr, cluster, leds, rooms)

    # инициализация цвета во всех модулях
    def init_colors(self) -> None:
        print('sending colors')
        for cluster in self.clusters:
            # print(cluster)
            self.construct_packet(cluster, STM32_command.set_colors)



    def monitor_clusters(self) -> None:
        # parse metrics data for each cluster
        # ask bd if any changes per mac (try to change status)
        # based on return value construct msg to stm, at the end update stm32
        # self.grafana.get_metrics() # grafana class updates bd
        for cluster in self.clusters:
            # get number of leds in cluster
            # get value by led id
            # print(cluster)
            if cluster == 'atrium':
                continue
            time.sleep(0.1)
            self.construct_packet(cluster, STM32_command.set_matrix)
            # print('sent matrix')

    def construct_packet(self, cluster, cmd) -> None:
        stm32 = self.clusters.index(cluster)
        leds = self.stm32[stm32].leds()
        rooms = self.stm32[stm32].rooms()
        i2c_array = [0] * (1 + leds + rooms)
        if cmd == STM32_command.set_matrix:
            #i2c_array = [None] * (6 + leds)
            i2c_array[0] = int(STM32_command.set_matrix)
            #i2c_array[0] = int(Status.FREE)
            #i2c_array[1] = int(Status.USED)
            #i2c_array[2] = int(Status.COVID)
            #i2c_array[3] = int(Status.EXAM)
            #i2c_array[4] = 0 # WTF
            #i2c_array[5] = self.getBrightnessLevel()
            self.fill_cluster_array(cluster, i2c_array, leds, rooms)

        # elif cmd == STM32_command.set_bright:
        #     i2c_array[0] = int(STM32_command.set_bright)
        #     i2c_array[1] = int(self.get_brightness())
        #     print(i2c_array)

        elif cmd == STM32_command.set_colors:
            i2c_array[0] = int(STM32_command.set_colors)
            i2c_array[1:4] = extract_color(colors.GREEN)
            i2c_array[4:7] = extract_color(colors.RED)
            i2c_array[7:10] = extract_color(colors.BLUE)
            i2c_array[10:13] = extract_color(colors.PURPLE)
            i2c_array[13:16] = extract_color(colors.WHITE)
            # print(i2c_array)
            # print(len(i2c_array))

        stm32_addr = self.stm32[stm32].addr()
        try:
            self.send_packet(stm32_addr, i2c_array)
        except:
            print("error sending packet!!!")
            pass

    def send_packet(self, addr, data):
        msg = i2c_msg.write(addr, data)
        self.bus.i2c_rdwr(msg)
        #data = data[32:]
        #if len(data) > 0:
        #    self.bus.write_i2c_block_data(addr, 0, data)

    # def fill_cluster_array(self, cluster, data, leds, rooms):
    #     for room in range(0, rooms):
    #         data[1+room] = 0
    #     for led in range(0, leds):
    #         data[1+rooms+led] = self.db.fetch_cluster_led_status(cluster, led)
    #         if not data[1+rooms+led]:
    #             data[1+rooms+led] = int(Status.COVID)
    #         #data[6+led] = self.db.fetch_cluster_led_status(cluster, led)
    #     # print(data)
    #     # print(len(data))
    #     # cluster_data = []
    #     # cluster_status = self.db.fetch_cluster_led_status(cluster, 3)
    #     # cluster_data = self.db.fetch_cluster_data(cluster, cluster_data)
    #     # print(cluster_status)
    #     # print(cluster_data)
    #     # self.db.change_mac_status(cluster, 'b2', 3)
    #     # cluster_status = self.db.fetch_cluster_led_status(cluster, 6)
    #     # print(cluster_status)




    # Запись в bus? пока не понятно как работает
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    

def main():
    # инициализация raspberry pi и модулей
    # TODO добавить в конфиги
    rpi = Master(clusters_conf.names)
    rpi.init_slaves()
    rpi.init_colors()

    # while True:
    #     try:
    #         rpi.construct_packet()
    #         # rpi.monitor_clusters()
    #         time.sleep(0.5)
    #     except:
    #         # TODO логи
    #         pass

if __name__ == "__main__":
    main()