from Code.complex import Complex
import enum
import math

class Branch(enum.Enum):
    POSITIVE = "C\[0, infinity)"
    NEGATIVE = "C\(-infinity, 0]"
    

def exponential(z: Complex) -> Complex:
    """
    Represents e^z as 
    e^z = e^{Re(z)} * e^{i * Im(z)} = e^{Re(z)} *(cos(Im(z)) + i * sin(Im(z)))=
    """
    return (math.e ** z.re) * Complex(re=math.cos(z.im), im=math.sin(z.im))

def distance(p: Complex, q: Complex) -> float:
    """
    Computes the distance between two complex points
    """
    return (p - q).modulus()

def is_point_in_branch(p: Complex, branch: Branch) -> bool:
    """
    Checks if a point lies along the real number line in
    the positive or negative branch
    """
    if p.im == 0:
        if branch == Branch.POSITIVE:
            return p.re >= 0
        elif branch == Branch.NEGATIVE:
            return p.re <= 0
        else:
            raise Exception(f"Unsupported branch {branch.value}")
    
    return False


def log(p: Complex, branch: Branch = Branch.POSITIVE):
    """
    Computes the complex logarithm on a specified branch of log (default positive)
    using the formula 
    log(p) = log(re^{i * theta})
           = log(r) + log(i * theta)
    
    log(|p|) + i * arg(p)
    """
    if not is_point_in_branch(p, branch):
        return Complex(
            re=math.log(p.modulus()),
            im=p.argument()
        )
        
    raise ValueError(
        f'The inputted point {p} is within the branch {branch}'
    )

def pow(p: Complex, q: Complex):
    """
    Computes p^q using the fact that p^q = e^{qlog(p)}
    """
    return exponential(q * log(p))    