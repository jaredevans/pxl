# main.py

#!/usr/bin/env python3
import sys
import select
import time
from PIL import Image
from color import rgb, term_color
from image import canvas_size, scale, img_area, avg_rgb

def draw(img):
    cols, rows, whratio = canvas_size()
    img_w, img_h = img.size
    img_scale = scale(img_w, img_h, cols, rows, whratio)

    # recompute canvas to match scaled image
    cols = int(img_w / img_scale)
    rows = int(img_h / (img_scale * whratio))

    # clear screen
    sys.stdout.write("\x1b[2J")
    for y in range(rows):
        for x in range(cols):
            sx, sy, ex, ey = img_area(x, y, img_scale, whratio)
            # upper half
            r1, g1, b1 = avg_rgb(img, sx, sy, ex, (sy + ey) // 2)
            # lower half
            r2, g2, b2 = avg_rgb(img, sx, (sy + ey) // 2, ex, ey)
            fg = term_color(r2, g2, b2)
            bg = term_color(r1, g1, b1)
            sys.stdout.write(f"\x1b[38;5;{fg}m\x1b[48;5;{bg}m▄")
        sys.stdout.write("\x1b[0m\n")
    sys.stdout.flush()

def display(path):
    try:
        img = Image.open(path).convert("RGB")
    except Exception as e:
        print(f"Error opening {path}: {e}", file=sys.stderr)
        return

    draw(img)

    # wait for 'q' or ESC
    import termios, tty
    old = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                ch = sys.stdin.read(1)
                if ch in ('q', '\x1b'):
                    break
            time.sleep(0.01)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image>...", file=sys.stderr)
        print("Press 'q' or ESC to quit.", file=sys.stderr)
        sys.exit(1)

    for imgfile in sys.argv[1:]:
        display(imgfile)

if __name__ == "__main__":
    main()
