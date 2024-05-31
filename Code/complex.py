# Defines the Complex Numbers and performs the necessary computations
import math
import fractions
from typing import Union


class Complex:
    """
    Defines the base class for representing complex numbers, alongside basic
    operations like addition, multiplication, subtraction, division, and
    """
    # the amount of decimal places to represent complex numbers
    DECIMAL_PLACES = 15
    def __init__(self, re, im) -> None:
        '''
        Initializes the Complex class which attempts to represent the complex 
        numbers in python
        '''
        [self.re, self.im] = map(lambda x: round(x, self.DECIMAL_PLACES), [re, im])
        
    def __clean_operation(self, other: any):
        '''
        Ensures the other parameter is a complex number when performing 
        operation. If it's an int or float we convert that to a complex number 
        and return it.
        '''
        if isinstance(other, int) or isinstance(other, float):
            return Complex(re=other, im=0)
        if isinstance(other, Complex):
            return other
        if not isinstance(other, Complex):
            raise ValueError(
                "You're trying to operate a complex number with a non-complex number"
            )
    
    def __convert_decimal_to_fraction(self, number: Union[float, int]) -> str:
        fraction = fractions.Fraction(number).limit_denominator()
        num = f"{'- ' if fraction.numerator < 0 else ''}{abs(fraction.numerator)}"
        if fraction.denominator == 1:
            return f"{num}"
        return f"{num}/{fraction.denominator}"
            
    def __repr__(self) -> str:
        '''
        Represents the complex number in a suitable format of a + i * b
        '''
        [
            real, imaginary
        ] = map(
            lambda x: self.__convert_decimal_to_fraction(x),
            [self.re, self.im]
        )
        if self.re == 0:
            return f"{imaginary} * i"
        if self.im == 0:
            return f"{real}"
            
        return f"{real}{' + ' if self.im > 0 else ' '}{imaginary} * i"
    
    def __float__(self):
        '''
        Converts a complex number into a float for arithmetic purposes
        '''
        if self.im != 0:
            raise TypeError(
                f"Cannot convert {self} to float since it has a non-zero imaginary part"
            )
            
        return float(self.re)
    
    def __eq__(self, other) -> bool:
        other = self.__clean_operation(other)
        return self.im == other.im and self.re == other.re
    
    def __neg__(self):
        return -1 * self
    
    def __pos__(self):
        return self
    
    def __mul__(self, other):
        '''
        Defines multiplication for complex numbers
        '''
        other = self.__clean_operation(other)
        return Complex(
            re=self.re * other.re - self.im * other.im, 
            im=self.re * other.im + other.re * self.im
        )
    
    def __rmul__(self, other):
        '''
        Defines right-handed multiplication. Since C is commutative under 
        multiplication we can return __mul__
        '''
        return self.__mul__(other)
    
    def __add__(self, other):
        '''
        Adds two complex numbers and returns a complex number
        '''
        other = self.__clean_operation(other)
        return Complex(re=self.re + other.re, im=self.im + other.im)
    
    def __radd__(self, other):
        '''
        Defines right-handed addition in C, which is equivalent to left handed
        addition since C is commutative under addition.
        '''
        return self.__add__(other)
    
    def __sub__(self, other):
        '''
        Computes self - other by adding self with -1 * other
        '''
        other = -1 * self.__clean_operation(other)
        return self + other
    
    def __rsub__(self, other):
        '''
        Computes other - self by adding other with -1 * self
        '''
        other = self.__clean_operation(other)
        return other - self
    
    def __truediv__(self, other):
        '''
        If p is self and q is other, then the function computes p / q using 
        the formula p / q = (p * conj(q)) / (q * conj(q)).
        
        But q * conj(q) = Re(q)^2 + Im(q)^2 which is real, so we
        '''
        other = self.__clean_operation(other)
        if other == Complex(0, 0):
            raise ZeroDivisionError(f"You're dividing ('{self}') by 0")
        
        conj_other = other.conjugate()
        divisor = float(other * conj_other)
        return conj_other * Complex(self.re / divisor, self.im / divisor)  
    
    def __rtruediv__(self, other):
        other = self.__clean_operation(other)
        return other / self
        
    def modulus(self):
        '''
        Returns the modulus of z = a + i * b by computing sqrt(z * conj(z))
        '''
        return math.sqrt(self * self.conjugate())
    
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
    
    def inverse(self):
        '''
        Computes z^-1 = 1 / z so long as z != 0
        '''
        return Complex(1, 0) / self
    
    def polar_form(self):
        r = self.modulus()
        theta = self.argument()
        ei_theta = Complex(math.cos(theta), math.sin(theta))
        return r * ei_theta
    
    def __pow__(self, n: int):
        '''
        Computes z^n by representing z as its polar form r * e^(i * theta), 
        where r and theta are z's modulus and argument, respectively. 
        
        Therefore, z^n = r^n * e^(i * n * theta)
        '''
        if not isinstance(n, int):
            raise ValueError(
                f"{n} is not an int. To work with powers for non integers, use
                ComplexFunctions.pow function with your complex numbers"
            )
            
        r = self.modulus()
        theta = self.argument()
        ei_theta = Complex(math.cos(n * theta), math.sin(n * theta))
        return (r ** n) * ei_theta

