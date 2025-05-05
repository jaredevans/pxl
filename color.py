# color.py

def rgb(color):
    """
    Take an (R,G,B) or (R,G,B,A) tuple with 8-bit channels (0–255)
    and return the (r, g, b) components.
    """
    r, g, b = color[:3]
    return r, g, b

def term_color(r, g, b):
    """
    Convert 8-bit r,g,b into a 256-color terminal code, with the same
    mapping as Go’s termColor (plus an offset of 16+1).
    """
    # map from 0–255 into 0–5
    r_term = (((r * 5) + 127) // 255) * 36
    g_term = (((g * 5) + 127) // 255) * 6
    b_term = (((b * 5) + 127) // 255)
    return r_term + g_term + b_term + 17  # 16 + 1 offset
