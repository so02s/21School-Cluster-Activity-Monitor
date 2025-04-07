import time
from utils.STM32 import STM32_addr, STM32_leds, STM32_rooms
from smbus2 import SMBus, i2c_msg
from utils.settings import STM32_command, clusters_conf, colors
from utils.colors import extract_color
# from utils.db import ClusterDB
from utils.school_api import SchoolClient
 
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
    def __init__(self, clusters: list, usr: str, psw: str) -> None:
        self.clusters = clusters
        self.num_of_clusters = len(clusters)

        # бд для пиров и трайбов
        # self.db = ClusterDB()
        # slaves
        self.stm32: list[STM32] = [None]*self.num_of_clusters
        # для шины i2c (взаимодействие с STM32)
        self.bus = SMBus(1)
        # взаимодействие с api платформы
        self.school_cli = SchoolClient(usr, psw)
        
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
            self.construct_packet(cluster, STM32_command.set_colors)


    def refresh_occupied_places(self) -> None:
        for i, cluster in enumerate(self.clusters):
            leds = self.stm32[i].leds()
            rooms = self.stm32[i].rooms()
            # инициализация данных для отправки на stm
            i2c_array = [0] * (1 + leds + rooms)
            # команда на перекрас
            i2c_array[0] = int(STM32_command.set_matrix)

            # i2c_array[1+rooms+led] = 0

            places: list = self.school_cli.get_map(cluster=cluster)
            for record in places:
                # if проверка есть ли такое имя в бд
                tribe = self.school_cli.get_tribe(record['login'])
                if tribe[0] == 'A':
                    col = extract_color(colors.GREEN)
                elif tribe[0] == 'C':
                    col = extract_color(colors.RED)
                elif tribe[0] == 'S':
                    col = extract_color(colors.PURPLE)
                elif tribe[0] == 'H':
                    col = extract_color(colors.BLUE)
                    
                led = self.place_to_led(cluster, record['row'], record['number'])
                i2c_array[1+rooms+led] = col

            self.send_packet(self.stm32[i].addr(), i2c_array)

            # places_tribes:list = self.db.check_tribes(places)

    def construct_packet(self, cluster, cmd) -> None:
        stm32 = self.clusters.index(cluster)
        leds = self.stm32[stm32].leds()
        rooms = self.stm32[stm32].rooms()
        i2c_array = [0] * (1 + leds + rooms)
        
        if cmd == STM32_command.set_colors:
            i2c_array[0] = int(STM32_command.set_colors)
            i2c_array[1:4] = extract_color(colors.GREEN)
            i2c_array[4:7] = extract_color(colors.RED)
            i2c_array[7:10] = extract_color(colors.BLUE)
            i2c_array[10:13] = extract_color(colors.PURPLE)
            i2c_array[13:16] = extract_color(colors.BLACK)

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

    # Запись в bus? пока не понятно как работает и для чего используется
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    
    def place_to_led(self, cluster, row, number):
        clusters = {
            "oa": [['a', 5], ['b', 6], ['c', 6], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6], ['l', 6], ['m', 6], ['n', 6], ['o', 4]], 
            'il' : [['a', 3], ['b', 4], ['c', 4], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6]], 
            'mi': [['a', 6], ['b', 6], ['c', 6], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6], ['l', 6], ['m', 6], ['n', 6], ['o', 6], ['p', 6], ['q', 6], ['r', 6], ['s', 6], ['t', 6], ['u', 6], ['v', 6], ['w', 6]], 
            'at': [['a', 2], ['b', 2], ['c', 3], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 7], ['j', 6], ['k', 8], ['l', 8], ['m', 8], ['n', 8], ['o', 9], ['p', 9], ['q', 9], ['r', 8]],
            'am': [['a', 5]]
        }

        for i, (r, n) in enumerate(clusters[cluster]):
            if r == row and n == number:
                return i
        return None
    

def main():
    # инициализация raspberry pi и модулей
    # TODO добавить в конфиги
    rpi = Master(clusters_conf.names)
    rpi.init_slaves()
    rpi.init_colors()

    while True:
        try:
            rpi.refresh_occupied_places()
            time.sleep(300)
        except:
            # TODO логи
            pass

if __name__ == "__main__":
    main()