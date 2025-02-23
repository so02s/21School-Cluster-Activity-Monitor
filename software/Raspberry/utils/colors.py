def extract_color(color):
    return (
        (color & 0xff0000) >> 16,  # R
        (color & 0x00ff00) >> 8,   # G
        (color & 0x0000ff)         # B
    )