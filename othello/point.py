//  Copyright © 2016 Oh Jun Kwon. All rights reserved.

import math

class Point:
    def __init__(self, frac_x, frac_y):
        self._frac_x = frac_x
        self._frac_y = frac_y


    def frac(self):
        return self._frac_x, self._frac_y


    def pixel(self, width, height):
        return self._frac_x * width, self._frac_y * height


    def frac_distance_from(self, p):
        return math.sqrt(
            (self._frac_x - p._frac_x)*(self._frac_x - p._frac_x)
            + (self._frac_y - p._frac_y)*(self._frac_y - p._frac_y)
            )


def from_frac(frac_x, frac_y):
    return Point(frac_x, frac_y)


def from_absolute(pixel_x, pixel_y, width, height):
    return Point(pixel_x/width, pixel_y/height)


