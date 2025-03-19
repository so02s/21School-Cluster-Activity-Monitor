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

class Ball:
    def __init__(self, cluster):
        self.cluster = cluster
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 1
        self.color = colors.BLUE

    def refresh_position(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x >= len(self.cluster) - 1:
            self.dx *= -1
        if self.y < 0 or self.y >= len(self.cluster[0]) - 1:
            self.dy *= -1

    def refresh_color(self):
        pass


class Master:
    def __init__(self, clusters: list) -> None:
        self.clusters = clusters
        self.num_of_clusters = len(clusters)
        # slaves
        self.stm32: list[STM32] = [None]*self.num_of_clusters
        # для шины i2c (взаимодействие с STM32)
        self.bus = SMBus(1)
        self.balls: list[Ball] = [None]*self.num_of_clusters

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

    def init_balls(self) -> None:
        for i, cluster in enumerate(self.clusters):
            if cluster == 'atrium':
                continue
            self.balls[i] = Ball(cluster)

    def monitor_clusters(self) -> None:
        for cluster in self.clusters:
            if cluster == 'atrium':
                continue
            time.sleep(0.1)
            self.construct_packet(cluster, STM32_command.set_matrix)

    def construct_packet(self, cluster, cmd) -> None:
        numb = self.clusters.index(cluster)
        leds = self.stm32[numb].leds()
        rooms = self.stm32[numb].rooms()
        ball = self.balls[numb]
        i2c_array = [0] * (1 + leds + rooms)

        if cmd == STM32_command.set_matrix:
            i2c_array[0] = int(STM32_command.set_matrix)
            self.fill_cluster_array(i2c_array, leds, rooms, ball)
        elif cmd == STM32_command.set_colors:
            i2c_array[0] = int(STM32_command.set_colors)
            for i in range(1, 16, 3):
                i2c_array[i:i+3] = extract_color(colors.BLACK)
        stm32_addr = self.stm32[numb].addr()
        try:
            self.send_packet(stm32_addr, i2c_array)
        except:
            # TODO логи
            print("error sending packet!!!")
            pass

    def send_packet(self, addr, data):
        msg = i2c_msg.write(addr, data)
        self.bus.i2c_rdwr(msg)

    def fill_cluster_array(self, data, leds, rooms, ball: Ball):
        for room in range(0, rooms):
            data[1+room] = 0
        # Тут передается значение конкретного светодиода
        for led in range(0, leds):
            if led == ball.x + ball.y:
                data[1+rooms+led] = ball.color
            data[1+rooms+led] = 0

    # Запись в bus? пока не понятно как работает и для чего используется
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    
    def refresh_ball(self):
        for ball in self.balls:
            ball.refresh_position()
            ball.refresh_color()

def main():
    rpi = Master(clusters_conf.names)
    rpi.init_slaves()
    rpi.init_colors()
    rpi.init_balls()

    while True:
        try:
            rpi.refresh_ball()
            rpi.monitor_clusters()
            time.sleep(0.5)
        except:
            # TODO логи
            pass


if __name__ == "__main__":
    main()


# 29 строк
# 26 столбцов

array = [[0 for _ in range(26)] for _ in range(29)]

for x, j in enumerate(array):
    for y, _ in enumerate(j):
        if (x>3 and x<18) and (y>=0 and y<6):
            array[x][y] = 1
        

for i in array:
    print(i)