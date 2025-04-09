import time
from utils.STM32 import STM32_addr, STM32_leds, STM32_rooms
from smbus2 import SMBus, i2c_msg
from utils import settings
from utils.colors import extract_color
from utils.db import DatabaseManager
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
        self.db = DatabaseManager()
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
            self.construct_packet(cluster, settings.STM32_command.set_colors)


    def refresh_occupied_places(self) -> None:
        print('setting matrix')
        for i, cluster in enumerate(self.clusters):
            self.construct_packet(cluster, settings.STM32_command.set_matrix)

    def check_api(self, cluster: str, i2c_array: list[int], rooms: int) -> None:
        places: list = self.school_cli.get_map(cluster=cluster)

        for record in places:
            tribe = self.db.get_user_tribe(record['login'])
            if not tribe:
                tribe = self.school_cli.get_tribe(record['login'])
                self.db.add_user(record['login'], tribe)

            # ALPACAS, CAPYBARS, SALAMANDRAS, HONEYBEARS
            tribe_colors = {'A': 1, 'C': 2, 'S': 4, 'H': 3}
            col = tribe_colors.get(tribe[0])
                
            led = self.place_to_led(cluster, record['row'], record['number'])
            i2c_array[1+rooms+led] = col
        print(i2c_array)


    def construct_packet(self, cluster: str, cmd) -> None:
        stm32 = self.clusters.index(cluster)
        leds = self.stm32[stm32].leds()
        rooms = self.stm32[stm32].rooms()
        i2c_array: list[int] = [0] * (1 + leds + rooms)
        
        if cmd == settings.STM32_command.set_colors:
            i2c_array[0] = int(settings.STM32_command.set_colors)
            i2c_array[1:4] = extract_color(settings.colors.GREEN)
            i2c_array[4:7] = extract_color(settings.colors.RED)
            i2c_array[7:10] = extract_color(settings.colors.BLUE)
            i2c_array[10:13] = extract_color(settings.colors.PURPLE)
            i2c_array[13:16] = extract_color(settings.colors.BLACK)
        elif cmd == settings.STM32_command.set_matrix:
            i2c_array[0] = int(settings.STM32_command.set_matrix)
            self.check_api(cluster, i2c_array, rooms)
            print(i2c_array)
            

        stm32_addr = self.stm32[stm32].addr()
        try:
            self.send_packet(stm32_addr, i2c_array)
        except:
            # TODO логи
            print("error sending packet!!!")
            pass

    def send_packet(self, addr, data):
        msg = i2c_msg.write(int(addr), data)
        self.bus.i2c_rdwr(msg)

    # Запись в bus? пока не понятно как работает и для чего используется
    def writeByte(self, address, value):
        self.bus.write_byte(address, value)
    def readByte(self, address):
        return self.bus.read_byte(address)
    
    def place_to_led(self, cluster, row, number):

        for i, (r, n) in enumerate(settings.clusters[cluster]):
            if r == row and n == number:
                return i
        return None
    
    def sitters(self):
        for cluster in self.clusters:
            print(cluster)
            places: list = self.school_cli.get_map(cluster=cluster)
            print(places)
            for record in places if places else []:
                tribe = self.db.get_user_tribe(record['login'])
                if not tribe:
                    tribe = self.school_cli.get_tribe(record['login'])
                    self.db.add_user(record['login'], tribe)
                print(record, tribe)

    

def main():
    rpi = Master(
        settings.clusters_conf.names,
        settings.school_api.USERNAME_SCHOOL,
        settings.school_api.PASSWORD_SCHOOL
    )
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