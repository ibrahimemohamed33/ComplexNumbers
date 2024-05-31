import math
import constants

from enum import Enum
from complex import Complex, distance, is_equal
from curves import triangle_length
from constants import Corner, corners


class Curve(Enum):
    CIRCLE = 0
    SQUARE = 1
    RECTANGLE = 2
    UPPER_SEMICIRCLE = 3
    LOWER_SEMICIRCLE = 4
    TRIANGLE = 5


def circle_length(radius: float):
    return 2 * math.pi * radius


def obtain_rect_point(center: Complex, radiusA: float, radiusB: float,
                      corner: constants.Corner) -> Complex:
    '''

    '''
    if corner == Corner.TopRight:
        x, y = radiusA, radiusB
    elif corner == Corner.BottomRight:
        x, y = radiusA, -radiusB
    elif corner == Corner.TopLeft:
        x, y = -radiusA, radiusB
    elif corner == Corner.BottomLeft:
        x, y = -radiusA, -radiusB
    else:
        raise Exception(f"Unsupported corner {corner.name}")

    return Complex(x + center.re, y + center.im)


def rect_points(center: Complex, radiusA: float, radiusB: float):
    return [obtain_rect_point(center, radiusA, radiusB, corner) for corner in corners]


def square_points(center: Complex, radius: float):
    return rect_points(center, radius, radius)


def rectangle_length(radiusA: float, radiusB: float):
    return constants.NUM_POINTS_RECT * (radiusA + radiusB)


def square_length(radius: float):
    return rectangle_length(radius, radius)


def valid_triangle(points: 'list[Complex]') -> None:
    if len(points) != constants.NUM_POINTS_TRIANGLE:
        raise Exception(
            f"You need {constants.NUM_POINTS_TRIANGLE} to form a triangle but only {len(points)} were given"
        )

    for point in points:
        for other_point in points:
            if not is_equal(point, other_point):
                pass
    pass


def triangle_length(points: 'list[Complex]'):
    # valid_triangle(points)

    total_length = 0
    for pointA in points:
        for pointB in points:
            if not is_equal(pointA, pointB):
                total_length += distance(pointA, pointB)
    return total_length


def curve_length(curve: Curve, radiusA=0, radiusB=0, points=[]):
    if curve == Curve.CIRCLE:
        return circle_length(radiusA)
    elif curve == Curve.LOWER_SEMICIRCLE or curve == Curve.UPPER_SEMICIRCLE:
        return circle_length(radiusA) / 2
    elif curve == Curve.SQUARE:
        return square_length(radiusA)
    elif curve == Curve.RECTANGLE:
        return rectangle_length(radiusA, radiusB)
    elif curve == Curve.TRIANGLE:
        return triangle_length(points)
    else:
        raise Exception(f"Unsupported curve type {curve.name}")
