# image.py

import sys
import fcntl
import termios
import struct

DEFAULT_RATIO = 7.0 / 3.0

def canvas_size():
    """
    Returns (cols, rows, width/height cursor ratio).
    Uses ioctl(TIOCGWINSZ) to get rows, cols, pixel_width, pixel_height.
    """
    fd = sys.stdout.fileno()
    s = struct.pack("HHHH", 0, 0, 0, 0)
    try:
        x = fcntl.ioctl(fd, termios.TIOCGWINSZ, s)
        rows, cols, pw, ph = struct.unpack("HHHH", x)
    except:
        rows = cols = pw = ph = 0

    whratio = DEFAULT_RATIO
    if rows > 0 and cols > 0 and pw > 0 and ph > 0:
        # same as Go: float(ph/rows) / float(pw/cols)
        whratio = (ph / rows) / (pw / cols)
    return cols, rows, whratio

def max_value(*values):
    """
    Return max(values, 1.0)
    """
    m = 0.0
    for v in values:
        if v > m:
            m = v
    return m if m >= 1.0 else 1.0

def scale(img_w, img_h, term_w, term_h, whratio):
    """
    Compute scale = max(img_h/(term_h*whratio), img_w/term_w, 1)
    """
    hr = img_h / (term_h * whratio)
    wr = img_w / term_w
    return max_value(hr, wr)

def img_area(term_x, term_y, img_scale, whratio):
    """
    Map terminal cell (term_x,term_y) → image rect (startX, startY, endX, endY)
    """
    start_x = term_x * img_scale
    start_y = term_y * img_scale * whratio
    end_x = start_x + img_scale
    end_y = start_y + img_scale * whratio
    return int(start_x), int(start_y), int(end_x), int(end_y)

def avg_rgb(img, start_x, start_y, end_x, end_y):
    """
    Average R,G,B over the given rectangle in a PIL Image (mode=RGB).
    """
    total_r = total_g = total_b = 0
    count = 0
    width, height = img.size

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if 0 <= x < width and 0 <= y < height:
                r, g, b = img.getpixel((x, y))
                total_r += r
                total_g += g
                total_b += b
                count += 1

    if count == 0:
        return 0, 0, 0
    return total_r // count, total_g // count, total_b // count
