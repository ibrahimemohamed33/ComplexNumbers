from enum import Enum

from Code.complex import Complex

i = Complex(0, 1)
ORIGIN = Complex(0, 0)
ONE = Complex(1, 0)
NEGATIVE_ONE = -ONE
NEGATIVE_i = -i

POSITIVE_BRANCH = "C\[0, infinity)"
NEGATIVE_BRANCH = "C\(-infinity, 0]"

DENOMINATOR = '/'
COMPLEX_VARIABLE = 'z'
EXPONENT = "^"
NUM_POINTS_TRIANGLE = 3
NUM_POINTS_RECT = 4
LEFT_FUNC_PARAM = '{'
RIGHT_FUNC_PARAM = '}'


class Corner(Enum):
    TopRight = 0
    BottomRight = 1
    TopLeft = 2
    BottomLeft = 3


corners = [Corner.TopRight, Corner.BottomRight, Corner.TopLeft,
           Corner.BottomLeft]
