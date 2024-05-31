from constants import *


class Function:
    def __init__(self, function: str, variable: str) -> None:
        '''
        Please see the documentation on how to input a readable function
        '''
        self.variable = variable
        self.function = self.simplify_function(function)

    def __repr__(self) -> str:
        return self.function

    def __clean_function(self, function: str):
        '''
        Cleans the function before its terms are simplified
        '''
        return function.replace(' ', '').replace('(', '').replace(')', '')

    def __reformat_function(self, components: 'list[str]'):
        '''
        Reformats the function
        '''
        return '(' + (" + ".join(components)) + ')'

    def __is_polynomial(self, f: str, index: int) -> bool:
        '''
        Checks if f is a polynomial
        '''
        return (
            (f[index] == self.variable and f[index - 1] != EXPONENT) and
            (f[index - 1] != LEFT_FUNC_PARAM and f[index + 1] != RIGHT_FUNC_PARAM)
        )

    def __extract_coefficient(self, function: str):
        components = function.replace(' ', '').split('*')
        coefficients = []
        for component in components:
            if self.variable + EXPONENT not in component:
                if self.variable in component and RIGHT_FUNC_PARAM in component:
                    coefficients.append(component)

        return ' * '.join(coefficients)

    def __compute_degree(self, function: str):
        '''
        Computes the degree of a single expression not containing any addition
        '''
        count = 0
        for index in range(len(function)):
            if self.__is_polynomial(function, index):
                if function[index + 1] != EXPONENT:
                    count += 1
                else:
                    count += int(function[index + 2])
        return count

    def __simplify_components(self, components):
        simplified_components = []
        for component in components:
            coeff = self.__extract_coefficient(component)
            deg = self.__compute_degree(component)
            variable_term = self.variable + EXPONENT
            degree_total = variable_term + (str(deg) if deg else str(0))

            if coeff:
                simplified_coeff = (coeff + ' * ')
            else:
                simplified_coeff = '1 * '

            simplified_components.append(simplified_coeff + degree_total)

        return sorted(simplified_components, key=lambda x: int(x[-1]))

    def simplify_function(self, function: str):
        '''
        Simplifies function into a suitable format to perform additional
        complex computations
        '''
        formatted_func = self.__clean_function(function).split(DENOMINATOR)

        if len(formatted_func) == 1:
            num = formatted_func[0]
            denom = ''

        elif len(formatted_func) == 2:
            [num, denom] = formatted_func

        else:
            raise Exception(f"""You inputted {len(formatted_func) - 1} {DENOMINATOR}
            into your function {function} when only 0 or 1 are supported""")

        numerator_components = self.__simplify_components(num.split('+'))
        numerator = self.__reformat_function(numerator_components)
        if not denom:
            return numerator

        denominator = self.__simplify_components(denom.split('+'))
        return numerator + DENOMINATOR + self.__reformat_function(denominator)


class AnalyticFunction(Function):
    def __init__(self, function: str, variable: str) -> None:
        super().__init__(function, variable)

    def __repr__(self) -> str:
        return self.function

    def __max_degree(self, function: str):
        '''
        Computes the degree of a formatted function by finding the largest polynomial
        degree of its terms
        '''
        return int(function.replace('(', '').replace(')', '')[-1])

    def approaches_zero(self):
        '''
        Checks if the function approaches zero when evaluated over a large curve 
        (e.g. circle, square) goes to zero.

        We also know || \integral(f) || <= len(region) * max(f).

        So if f is a simple, entire rational function of two complex polynomials, then
        we know it is equivalent to the ratio of its largest terms for sufficiently
        large z. Moreover, the length of these regions is proportional to a linear factor,
        so we want to make sure the degree of the numerator + 1 < degree of denominator
        '''
        if DENOMINATOR not in self.function:
            return False

        denom_index = self.function.find(DENOMINATOR)
        num_degree = self.__max_degree(self.function[1:denom_index])
        denom_degree = self.__max_degree(self.function[denom_index + 1:])
        return num_degree + 1 < denom_degree

    def find_zeroes(self, function: str):
        '''
        \C is algebraically closed so all zeroes of a polynomial are contained in
        \C. In addition, we use the property that if \alpha is a root, then 
        its conjugate is also a root.
        '''
        # the zeroes of function are the zeroes of its numerator
        if DENOMINATOR in function:
            numerator = function.split(DENOMINATOR)[0]
            function = numerator
