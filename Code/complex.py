# Defines the Complex Numbers and performs the necessary computations
import math

from fractions import Fraction
from constants import ORIGIN, exponential


def represent_complex_number(re: float, im: float) -> str:
    '''
    Represents the complex number in a suitable format of a + i * b
    '''
    frac_re, frac_im = Fraction(re), Fraction(im)
    re_rep = f"({frac_re.numerator} / {frac_re.denominator})"
    im_rep = f"({frac_im.numerator} / {frac_im.denominator})"

    if im < 0:
        if re == 0:
            return f"- i * ({-frac_im.numerator} / {frac_im.denominator})"
        return f"{re_rep} /  - i * ({-frac_im.numerator} / {frac_im.denominator})"
    if im == 0:
        return f"{re_rep}"

    if re == 0:
        return f"i * {im_rep}"
    return f"{re_rep} + i * {im_rep}"


class Complex:
    def __init__(self, re, im) -> None:
        '''
        Initializes the Complex class which attempts to represent the complex 
        numbers in python
        '''
        self.re, self.im = re, im

    def __repr__(self) -> str:
        represent_complex_number(self.re, self.im)

    def modulus(self):
        '''
        Returns the modulus of z = a + i * b using the formula \sqrt(a^2 + b^2)
        '''
        return math.sqrt(self.re**2 + self.im**2)

    def argument(self):
        '''
        Returns the argument of a function between [-pi / 2, pi / 2]. If z == 0,
        then it's undefined. 
        '''
        if self.re != 0:
            return math.atan(self.im / self.re)

        if self.im > 0:
            return math.pi / 2

        if self.im < 0:
            return -math.pi / 2

    def conjugate(self):
        '''
        Returns the conjugate of z = a + ib as z_bar = a - ib
        '''
        return Complex(self.re, -self.im)

    def power(self, n: int):
        '''
        Computes z^n using the fact that z = r * e^(i * theta), where r and theta
        is z's modulus and argument, respectively. Therefore, z^n = r^n * e^(i * n * theta)
        '''
        return polar_form(self.modulus() ** n, self.argument() * n)

    def inverse(self):
        '''
        Computes z^-1 using the formula z^-1 = congjugate(z) / |z|^2 in C^*
        If z == 0, then it has no multiplicative inverse
        '''
        if not is_equal(self, ORIGIN):
            return multiply(real(1 / self.modulus() ** 2), self.conjugate())


def real(real_number: float):
    '''
    Embeds the real number into the complex plane
    '''
    return Complex(real_number, 0)


def lexiographic_order(p: Complex, q: Complex) -> bool:
    '''
    Checks if p > q lexiographically in the complex plane
    '''
    return (p.re > q.re) or (p.re == q.re and p.im > q.im)


def is_equal(p: Complex, q: Complex) -> bool:
    '''
    Checks if p, q \in C are equal
    '''
    return p.re == q.re and p.im == q.im


def distance(p: Complex, q: Complex) -> float:
    '''
    Computes the Euclidean Distance between two points p, q \in C
    '''
    return subtraction(p, q).modulus()


def addition(p: Complex, q: Complex) -> Complex:
    return Complex(p.re + q.re, p.im + q.im)


def subtraction(p: Complex, q: Complex) -> Complex:
    return Complex(p.re - q.re, p.im - q.im)


def multiply(p: Complex, q: Complex) -> Complex:
    return Complex(p.re * q.re - p.im * q.im, p.re * q.im + q.re * p.im)


def polar_form(radius: float, theta: float):
    '''
    Returns the polar form of z \in C of the form re^(i * theta)
    '''
    return multiply(real(radius), exponential(theta))
