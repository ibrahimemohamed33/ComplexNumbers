# Defines the Complex Numbers and performs the necessary computations
import math

POSITIVE_BRANCH = "C\[0, infinity)"
NEGATIVE_BRANCH = "C\(-infinity, 0]"


def represent_complex_number(re: float, im: float) -> str:
    '''
    Represents the complex number in a suitable format of a + i * b
    '''
    real, imaginary = round(re, 10), round(im, 10)

    if imaginary < 0:
        if real == 0:
            return f"- i * {-imaginary}"
        return f"{real} - i * {-imaginary}"
    if imaginary == 0:
        return f"{real}"

    if real == 0:
        return f"i * {imaginary}"
    return f"{real} + i * {imaginary}"


class Complex:
    def __init__(self, re, im) -> None:
        '''
        Initializes the Complex class which attempts to represent the complex 
        numbers in python
        '''
        self.re, self.im = re, im

    def __repr__(self) -> str:
        return represent_complex_number(self.re, self.im)

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


def addition(p: Complex, q: Complex) -> Complex:
    '''
    Adds the complex numbers p, q \in C
    '''
    return Complex(p.re + q.re, p.im + q.im)


def subtraction(p: Complex, q: Complex) -> Complex:
    '''
    Subtracts the complex numbers p, q \in C
    '''
    return Complex(p.re - q.re, p.im - q.im)


def multiply(p: Complex, q: Complex) -> Complex:
    '''
    Multiplies the complex numbers p, q \in C
    '''
    return Complex(p.re * q.re - p.im * q.im, p.re * q.im + q.re * p.im)


def divide(p: Complex, q: Complex) -> Complex:
    '''
    Computes p / q using the formula p / q = (p * conj(q)) / |q|^2
    '''
    denominator = real(1 / (q.modulus() ** 2))
    numerator = multiply(p, q.conjugate())
    return multiply(numerator, denominator)


def exponential(theta: float or Complex) -> Complex:
    '''
    Represents e^(i * theta) = cos(theta) + i * sin(theta)
    '''
    return Complex(math.cos(theta), math.sin(theta))


def polar_form(radius: float, theta: float):
    '''
    Returns the polar form of z \in C of the form re^(i * theta)
    '''
    return multiply(real(radius), exponential(theta))


def lexiographically_greater(p: Complex, q: Complex) -> bool:
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


def point_in_branch(p: Complex, branch: str):
    '''
    Checks if p \in C lies on a branch of C
    '''
    if p.im == 0:
        if branch == POSITIVE_BRANCH:
            return p.re >= 0
        elif branch == NEGATIVE_BRANCH:
            return p.re <= 0
        else:
            raise Exception(f"Unsupported branch {branch}")

    return False


def complex_log(p: Complex, branch: str):
    '''
    Computes the complex logarithm on a specified branch of log
    using the formula log(z) = log(|z|) + i * arg(z)
    '''
    if not point_in_branch(p, branch):
        return Complex(math.log(p.modulus()), p.argument())

    raise Exception(
        f'The inputted point {p} is within the branch {branch}')


def complex_exponential(p: Complex):
    '''
    Computes the complex exponential using the formula e^(x + iy) = e^x * e^(iy)
    for p = x + iy
    '''
    return multiply(real(math.exp(p.re)), exponential(p.im))


def random_expo(p: Complex, q: Complex, branch=POSITIVE_BRANCH) -> Complex:
    '''
    Computes p^q using the fact that p^q = e^{qlog(p)}
    '''
    return complex_exponential(multiply(q, complex_log(p, branch)))


def complex_sine(p: Complex):
    '''
    Computes the function sin(p) = (e^(ip) - e^(-ip)) / 2i for p \in C
    '''
    denominator = divide(ONE, Complex(0, 2))
    numerator = subtraction(complex_exponential(multiply(i, p)),
                            complex_exponential(multiply(neg_i, p)))

    return multiply(denominator, numerator)


def complex_cosine(p: Complex):
    '''
    Computes the function cos(p) = (e^(ip) + e^(-ip)) / 2 for p \in C
    '''
    denominator = real(1 / 2)
    numerator = addition(complex_exponential(multiply(i, p)),
                         complex_exponential(multiply(neg_i, p)))

    return multiply(denominator, numerator)


def i_power(n: int):
    '''
    Computes i^n recursively
    '''
    return ONE if n % 4 == 0 else multiply(i, i_power(n - 1))


i, neg_i = Complex(0, 1), Complex(0, -1)
ORIGIN, ONE = Complex(0, 0), Complex(1, 0)
