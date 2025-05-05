# test_color.py

import pytest
from color import rgb, term_color

def test_rgb_black():
    assert rgb((0, 0, 0)) == (0, 0, 0)

def test_rgb_white():
    assert rgb((255, 255, 255)) == (255, 255, 255)

def test_rgb_red():
    assert rgb((255, 0, 0)) == (255, 0, 0)

def test_term_color_black():
    # expect 16 (black) + 1
    assert term_color(0, 0, 0) == 17

def test_term_color_white():
    # expect 231 (white cube) + 1 = 232
    assert term_color(255, 255, 255) == 232

def test_term_color_red():
    # expect 196 (red cube) + 1 = 197
    assert term_color(255, 0, 0) == 197
