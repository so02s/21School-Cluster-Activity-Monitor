from betterconf import betterconf, Alias
from dotenv import load_dotenv

@betterconf
class STM32_addr_conf():
    oasis: Alias[int, "OASIS_ADDR"]
    mirage: Alias[int, "MIRAGE_ADDR"]
    illusion: Alias[int, "ILLUSION_ADDR"]
    atlantis: Alias[int, "ATLANTIS_ADDR"]
    atrium: Alias[int, "ATRIUM_ADDR"]

@betterconf
class STM32_leds_conf():
    oasis: Alias[int, "OASIS_LEDS"]
    mirage: Alias[int, "MIRAGE_LEDS"]
    illusion: Alias[int, "ILLUSION_LEDS"]
    atlantis: Alias[int, "ATLANTIS_LEDS"]
    atrium: Alias[int, "ATRIUM_LEDS"]

@betterconf
class STM32_rooms_conf():
    oasis: Alias[int, "OASIS_ROOM_COUNT"]
    mirage: Alias[int, "MIRAGE_ROOM_COUNT"]
    illusion: Alias[int, "ILLUSION_ROOM_COUNT"]
    atlantis: Alias[int, "ATLANTIS_ROOM_COUNT"]
    atrium: Alias[int, "ATRIUM_ROOM_COUNT"]

load_dotenv()

STM32_addr = STM32_addr_conf()
STM32_leds = STM32_leds_conf()
STM32_rooms = STM32_rooms_conf()
