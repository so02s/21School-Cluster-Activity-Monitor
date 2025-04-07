from betterconf import betterconf, Alias
from dotenv import load_dotenv

@betterconf
class STM32_addr_conf():
    oa: Alias[int, "OASIS_ADDR"]
    mi: Alias[int, "MIRAGE_ADDR"]
    il: Alias[int, "ILLUSION_ADDR"]
    at: Alias[int, "ATLANTIS_ADDR"]
    am: Alias[int, "ATRIUM_ADDR"]

@betterconf
class STM32_leds_conf():
    oa: Alias[int, "OASIS_LEDS"]
    mi: Alias[int, "MIRAGE_LEDS"]
    il: Alias[int, "ILLUSION_LEDS"]
    at: Alias[int, "ATLANTIS_LEDS"]
    am: Alias[int, "ATRIUM_LEDS"]

@betterconf
class STM32_rooms_conf():
    oa: Alias[int, "OASIS_ROOM_COUNT"]
    mi: Alias[int, "MIRAGE_ROOM_COUNT"]
    il: Alias[int, "ILLUSION_ROOM_COUNT"]
    at: Alias[int, "ATLANTIS_ROOM_COUNT"]
    am: Alias[int, "ATRIUM_ROOM_COUNT"]

load_dotenv()

STM32_addr = STM32_addr_conf()
STM32_leds = STM32_leds_conf()
STM32_rooms = STM32_rooms_conf()
