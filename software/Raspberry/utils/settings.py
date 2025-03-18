from betterconf import betterconf, Alias

@betterconf
class STM32ComandConfig:
    set_matrix: Alias[int, "COMMAND_SET_MATRIX"]
    set_colors: Alias[int, "COMMAND_SET_COLORS"]
    set_bright: Alias[int, "COMMAND_SET_BRIGHTNESS"]

@betterconf
class ColorsConfig:
    GREEN: int
    RED: int
    PURPLE: int
    BLUE: int
    WHITE: int
    BLACK: int

@betterconf
class ClustersConfig:
    names: Alias[list, "CLUSTERS"]


clusters_conf = ClustersConfig()
STM32_command = STM32ComandConfig()
colors = ColorsConfig()

# для настройки бд
Clusters = {
    "oasis": [['a', 5], ['b', 6], ['c', 6], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6], ['l', 6], ['m', 6], ['n', 6], ['o', 4]], 
    'illusion' : [['a', 3], ['b', 4], ['c', 4], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6]], 
    'mirage': [['a', 6], ['b', 6], ['c', 6], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 6], ['j', 6], ['k', 6], ['l', 6], ['m', 6], ['n', 6], ['o', 6], ['p', 6], ['q', 6], ['r', 6], ['s', 6], ['t', 6], ['u', 6], ['v', 6], ['w', 6]], 
    'atlantis': [['a', 2], ['b', 2], ['c', 3], ['d', 6], ['e', 6], ['f', 6], ['g', 6], ['h', 6], ['i', 7], ['j', 6], ['k', 8], ['l', 8], ['m', 8], ['n', 8], ['o', 9], ['p', 9], ['q', 9], ['r', 8]],
    'atrium': [['a', 5]]
}