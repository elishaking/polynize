from itertools import zip_longest


class Polynomial:
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        if kwargs.__contains__("order"):
            self.args = []
            for i in range(kwargs["order"] + 1):
                self.args.append(kwargs["coeff"] if i == 0 else 0)

    def nonz(self, arr: list):
        """
        Function nonz accepts a list and iterates iterate through the list to pass a non-zero value in the list(used
        for just the first non-zero value
        :param arr: list
        :return: non-zero value
        """
        for i in range(len(arr)):
            if arr[i] == 0:
                continue
            else:
                return arr[i]

    @staticmethod
    def augment(arr1: list, arr2: list) -> list:
        """
        :param arr1:list
        :param arr2:list
        :return:appends zero to the beginning of the list of smaller size before subtracting dividend from remainder
        """
        for i in range(len(arr2) - len(arr1)):
            if arr2[i] == 0:
                arr1 = [0] + arr1
            else:
                break
        return arr1

    def add_or_subtract(self, arr1: list, arr2: list, num: int):
        """
        :param arr1: list
        :param arr2: list
        :param num: constant to tell add_or_subtract function to add or subtract
        :return: arr1 + arr2 or arr1 - arr2
        """
        # If statement to determine the smaller array(or list) between self.args and other.args

        if len(arr1) < len(arr2):
            min_arr = arr1
            max_arr = arr2
        else:
            min_arr = arr2
            max_arr = arr1
        min_arr = self.new_array(len(min_arr), len(max_arr), min_arr)
        result = []  # result is an array used to store the result
        if len(arr1) == 1 or len(arr2) == 1:
            if len(arr1) == 1:
                result.append([b + arr1[0] for b in arr2]) if num == 0 else result.append([b - arr1[0] for b in arr2])
                return Polynomial(*result)
            elif len(arr2) == 1:
                result.append([b + arr2[0] for b in arr1]) if num == 0 else result.append([b - arr2[0] for b in arr1])
                return Polynomial(*result)
            else:
                result.append(arr1[0] + arr2[0]) if num == 0 else result.append(arr1[0]-arr2[0])
                return Polynomial(*result)
        for i in range(len(max_arr)):
            result.append(min_arr[i] + max_arr[i]) if num == 0 else result.append(min_arr[i] - max_arr[i])
        return Polynomial(*result)

    @staticmethod
    def new_array(min_len: int, max_len: int, arr: list) -> list:
        """
        :param min_len: length of small list
        :param max_len: length of big list
        :param arr: small list
        :return: new list equal in size with big list by appending zero to beginning of big list
        """
        new_len = max_len - min_len
        new_arr = list(arr)
        for i in range(new_len):
            new_arr = [0] + new_arr
        return new_arr

    def __add__(self, other):
        return self.add_or_subtract(self.args, other.args, 0)

    def __sub__(self, other):
        return self.add_or_subtract(self.args, other.args, 1)

    def __neg__(self):
        self.args = [-arg for arg in self.args]
        return self

    @staticmethod
    def multiply_polynomial(cp1: float, op1: float, cp2: float, op2: float):
        return Polynomial(coeff=cp1 * cp2, order=op1 + op2)

    def __mul__(self, other):
        # if len(self.args) == 1 or len(other.args) == 1:
        #     if len(self.args) == 1:
        #         total_after_multiplication += [b * self.args[0] for b in other.args]
        #         return Polynomial(total_after_multiplication)
        #     elif len(other.args) == 1:
        #         total_after_multiplication += ([b * other.args[0] for b in self.args])
        #         return total_after_multiplication
        #     else:
        #         total_after_multiplication += (self.args[0] * other.args[0])
        #         return total_after_multiplication
        if type(other) != Polynomial:
            return Polynomial(*[other * arg for arg in self.args])
        else:
            total_after_multiplication = Polynomial(0)
            for i in range(len(self)):
                mp = Polynomial(0)
                for j in range(len(other)):
                    mp += Polynomial.multiply_polynomial(self.args[i], len(self) - 1 - i, other.args[j], len(other) - 1 - j)
                total_after_multiplication += mp

            return total_after_multiplication

    def __pow__(self, power, modulo=None):
        exponent = Polynomial(1)
        for i in range(power):
            exponent *= self

        return exponent

    def __truediv__(self, other):
        i = 0
        quotient = []
        dividend = self.args
        if len(self.args) == 1 or len(other.args) == 1:
            if len(self.args) == 1:
                quotient.append([round(b / self.args[0]) for b in other.args])
                return Polynomial(*quotient)
            elif len(other.args) == 1:
                quotient.append([round(b / other.args[0]) for b in self.args])
                return Polynomial(*quotient)
            else:
                quotient.append(round(self.args[0] / other.args[0]))
                return Polynomial(*quotient)

        for k in range(len(self.args) - 1):
            if all(a == 0 for a in dividend):
                break
            else:
                quotient.append(self.nonz(dividend) / other.args[i])
                current_quotient = self.nonz(dividend) / other.args[i]
                current_remainder = [a * current_quotient for a in other.args]
                current_remainder = self.augment(current_remainder, dividend)
                dividend = [x - y for x, y in zip_longest(dividend, current_remainder, fillvalue=0)]
                quotient = tuple(quotient)
                dividend = tuple(dividend)

        return [Polynomial(*quotient), Polynomial(*dividend)]

    def __mod__(self, other):
        return self.__truediv__(other)[1]

    def __str__(self):
        return str('Polynomial({0})'.format(self.args))

    def __len__(self):
        return len(self.args)


if __name__ == '__main__':
    x = Polynomial(10, 10)
    x2 = Polynomial(0)
    print('x / x =', (x / x)[0])
    print('x * x =', x * 2)
