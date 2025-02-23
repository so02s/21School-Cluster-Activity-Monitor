

from configparser import ConfigParser

config = ConfigParser()
config.read('/home/pi/git/software/Raspberry/config.ini')
OASIS_ADDR = int(config.get('settings', 'OASIS_ADDR'))
MIRAGE_ADDR = int(config.get('settings', 'MIRAGE_ADDR'))
ILLUSION_ADDR = int(config.get('settings', 'ILLUSION_ADDR'))
ATLANTIS_ADDR = int(config.get('settings', 'ATLANTIS_ADDR'))
ATRIUM_ADDR = int(config.get('settings', 'ATRIUM_ADDR'))

STM32_addr = {"oasis": OASIS_ADDR, "illusion": ILLUSION_ADDR, "mirage": MIRAGE_ADDR, "atlantis": ATLANTIS_ADDR, "atrium":  ATRIUM_ADDR}

OASIS_LEDS = int(config.get('settings', 'OASIS_LEDS'))
MIRAGE_LEDS = int(config.get('settings', 'MIRAGE_LEDS'))
ILLUSION_LEDS = int(config.get('settings', 'ILLUSION_LEDS'))
ATLANTIS_LEDS = int(config.get('settings', 'ATLANTIS_LEDS'))
ATRIUM_LEDS = int(config.get('settings', 'ATRIUM_LEDS'))

STM32_leds = {"oasis": OASIS_LEDS, "illusion": ILLUSION_LEDS, "mirage": MIRAGE_LEDS, "atlantis": ATLANTIS_LEDS, "atrium":  ATRIUM_LEDS}

OASIS_ROOM_COUNT = int(config.get('settings', 'OASIS_ROOM_COUNT'))
MIRAGE_ROOM_COUNT = int(config.get('settings', 'MIRAGE_ROOM_COUNT'))
ILLUSION_ROOM_COUNT = int(config.get('settings', 'ILLUSION_ROOM_COUNT'))
ATLANTIS_ROOM_COUNT = int(config.get('settings', 'ATLANTIS_ROOM_COUNT'))
ATRIUM_ROOM_COUNT = int(config.get('settings', 'ATRIUM_ROOM_COUNT'))


STM32_rooms = {"oasis": OASIS_ROOM_COUNT, "illusion": ILLUSION_ROOM_COUNT, "mirage": MIRAGE_ROOM_COUNT, "atlantis": ATLANTIS_ROOM_COUNT, "atrium":  ATRIUM_ROOM_COUNT}
