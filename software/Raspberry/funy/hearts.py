import time
from utils.STM32 import STM32_addr, STM32_leds, STM32_rooms
from smbus2 import SMBus, i2c_msg
from utils.Grafana import Grafana
from utils.settings import STM32_command, clusters_conf, colors
from utils.colors import extract_color
from utils.db import ClusterDB
 
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
        # slaves
        self.stm32: list[STM32] = [None]*self.num_of_clusters
        # для шины i2c (взаимодействие с STM32)
        self.bus = SMBus(1)

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
        for cluster in self.clusters:
            if cluster == 'atrium':
                continue
            time.sleep(0.1)
            self.construct_packet(cluster, STM32_command.set_matrix)

    def construct_packet(self, cluster, cmd) -> None:
        stm32 = self.clusters.index(cluster)
        leds = self.stm32[stm32].leds()
        rooms = self.stm32[stm32].rooms()
        i2c_array = [0] * (1 + leds + rooms)

        if cmd == STM32_command.set_matrix:
            i2c_array[0] = int(STM32_command.set_matrix)
            self.fill_cluster_array(i2c_array, leds, rooms)
        elif cmd == STM32_command.set_colors:
            i2c_array[0] = int(STM32_command.set_colors)
            for i in range(1, 16, 3):
                i2c_array[i:i+3] = extract_color(colors.BLACK)
        stm32_addr = self.stm32[stm32].addr()
        try:
            self.send_packet(stm32_addr, i2c_array)
        except:
            # TODO логи
            print("error sending packet!!!")
            pass

    def send_packet(self, addr, data):
        msg = i2c_msg.write(addr, data)
        self.bus.i2c_rdwr(msg)

    def fill_cluster_array(self, data, leds, rooms):
        heart_shape = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ]

        for i in range(leds):
            for j in range(rooms):
                if heart_shape[i % len(heart_shape)][j % len(heart_shape[0])]:
                    data[1 + i + j * leds] = 1
                else:
                    data[1 + i + j * leds] = 0

        for room in range(0, rooms):
            data[1+room] = 0
        for led in range(0, leds):
            data[1+rooms+led] = 1 # Тут передается значение конкретного пина

    # Запись в bus? пока не понятно как работает и для чего используется
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    

def main():
    rpi = Master(clusters_conf.names)
    rpi.init_slaves()
    rpi.init_colors()

    while True:
        try:
            rpi.check_occupied_places()
            rpi.check_tribes()
            rpi.send_fill_clusters()
            time.sleep(0.5)
        except:
            # TODO логи
            pass


if __name__ == "__main__":
    main()