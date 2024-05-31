# import math
# from enum import Enum
# from analytic import ComplexFunction

# from complex import ORIGIN, Complex, distance
# from constants import LARGE_RADIUS


# class Curve(Enum):
#     SQUARE = 1
#     CIRCLE = 2
#     TRIANGLE = 3
#     UPPER_SEMICIRCLE = 4
#     LOWER_SEMICIRCLE = 5
#     RECTANGLE = 6


# def is_valid_triangle(distanceA: float, distanceB: float, distanceC: float):
#     '''
#     Checks if three distances satisfy the triangle inequality
#     '''
#     return (
#         (abs(distanceA - distanceC) <= distanceB <= distanceA + distanceC) and
#         (abs(distanceB - distanceC) <= distanceA <= distanceB + distanceC) and
#         (abs(distanceB - distanceA) <= distanceC <= distanceB + distanceA)
#     )


# def circle_length(radius: float):
#     '''
#     Returns the length of a circle
#     '''
#     return 2 * math.pi * radius


# def triangle_length(pointA: Complex, pointB: Complex, pointC: Complex):
#     '''
#     Returns the length of a triangle
#     '''
#     distAB, distAC = distance(pointA, pointB), distance(pointA, pointC)
#     distBC = distance(pointB, pointC)
#     if not is_valid_triangle(distAB, distAC, distBC):
#         raise Exception("No triangle can exist with these points")

#     return distAB + distAC + distBC


# def rectangle_length(pointA: Complex, pointB: Complex, pointC: Complex):
#     '''
#     Computes the length of the rectangle

#         A--------B
#         |        |
#         D--------C
#     '''
#     return 2 * (triangle_length(pointA, pointB, pointC) - distance(pointA, pointC))


# class Region:
#     def __init__(self, curve: Curve, center: Complex, radius: float, points: 'list[Complex]' or None):
#         self.curve = curve
#         self.center = center
#         self.radius = radius
#         self.points = points

#     def curve_length(self) -> float:
#         '''
#         Returns the length of a closed curve
#         '''

#         if self.curve == Curve.CIRCLE:
#             return circle_length(self.radius)
#         elif self.curve in [Curve.UPPER_SEMICIRCLE, Curve.LOWER_SEMICIRCLE]:
#             return circle_length(self.radius / 2)

#         elif self.curve == Curve.SQUARE:
#             points = points_from_info(self.center, self.radius, self.radius)
#             return 4 * self.radius
#         elif self.curve == Curve.TRIANGLE and len(self.points) == 3:
#             [pointA, pointB, pointC] = self.points
#             return triangle_length(pointA, pointB, pointC)
#         else:
#             raise Exception(
#                 f"Unsupported curve {self.curve.name} with the points {self.points}")

#     def integral(self, function: ComplexFunction):
#         # f_R = function.evaluate()
#         pass


# def points_from_info(center: Complex, lengthA: float, lengthB: float:
#     pass
