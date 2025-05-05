# test_image.py

import pytest
from image import max_value, scale

def test_max_value():
    assert max_value(1, 2, 3, 4, 5) == 5.0

def test_scale_up():
    # 4x4 image into 2x2 terminal ⇒ scale = 2
    assert scale(4, 4, 2, 2, 1) == 2.0

def test_scale_down():
    # 2x2 image into 4x4 terminal ⇒ scale = 1
    assert scale(2, 2, 4, 4, 1) == 1.0

def test_scale_custom_ratio():
    # 4x4 image into 2x1 terminal with whratio=2 ⇒ scale = 2
    assert scale(4, 4, 2, 1, 2) == 2.0
