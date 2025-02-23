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

@betterconf
class ClustersConfig:
    names: Alias[list, "CLUSTERS"]


clusters_conf = ClustersConfig()
STM32_command = STM32ComandConfig()
colors = ColorsConfig()
