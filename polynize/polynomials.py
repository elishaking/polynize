class Polynomial:

    from itertools import izip_longest

    def nonz(self, arr):
        '''
        Function nonz accepts a list and iterates iterate through the list to pass a non-zero value in the list(used for just the first non-zero value
        :param arr: list
        :return: non-zero value
        '''
        for i in range(len(arr)):
            if arr[i] == 0:
                continue
            else:
                return arr[i]

    @staticmethod
    def augment(arr1, arr2):
        '''
        :param arr1:list
        :param arr2:list
        :return:appends zero to the beginning of the list of smaller size before subtracting dividend from remainder
        '''
        for i in range(len(arr2)-len(arr1)):
            if arr2[i] == 0:
                arr1 = [0] + arr1
            else:
                break
        return arr1

    def add_or_subtract(self, arr1, arr2, num):
        '''
        :param arr1: list
        :param arr2: list
        :param num: constant to tell add_or_subtract function to add or subtract
        :return: arr1 + arr2 or arr1 - arr2
        '''
        # If statement to determine the smaller array(or list) between self.args and other.args
        if len(arr1) < len(arr2):
            minarr = arr1
            maxarr = arr2
        else:
            minarr = arr2
            maxarr = arr1
        minarr = self.new_array(len(minarr), len(maxarr),minarr)
        result = []  #result is an array used to store the result
        for i in range(len(maxarr)):
            result.append(minarr[i] + maxarr[i]) if num == 0 else result.append(minarr[i] - maxarr[i])

        return Polynomial(*result)

    def __init__(self, *args, **kwargs):
        self.args = args
        if kwargs.__contains__("order"):
            self.args = []
            for i in range(kwargs["order"]+1):
                self.args.append(kwargs["coeff"] if i == 0 else 0)

    def new_array(self, min_len, max_len, arr):
        '''
        :param min_len: length of small list
        :param max_len: length of big list
        :param arr: small list
        :return: new list equal in size with big list by appending zero to beginning of big list
        '''
        new_len = max_len - min_len
        new_arr = list(arr)
        for i in range(new_len):
            new_arr = [0] + new_arr
        return new_arr

    def __add__(self, other):
        self.add_or_subtract(self.args, other.args, 0)

    def __str__(self):
        return str(self.args)

    def __len__(self):
        return len(self.args)

    @staticmethod
    def multiply_polynomial(cp1, op1, cp2, op2):
        return Polynomial(coeff=cp1 * cp2, order=op1 + op2)

    def __mul__(self, other):
        total_after_multiplication = Polynomial(0)
        for i in range(len(self)):
            mp = Polynomial(0)
            for j in range(len(other)):
                mp += Polynomial.multiply_polynomial(self.args[i], len(self) - 1 - i, other.args[j], len(other) - 1 - j)
            total_after_multiplication += mp

        return total_after_multiplication

    def __div__(self, other):
        i = 0
        quotient = []
        dividend = self.args
        for k in range(len(self.args)-1):
            if all(a == 0 for a in dividend):
                break
            else:
                quotient.append(self.nonz(dividend) / other.args[i])
                current_quotient = self.nonz(dividend) / other.args[i]
                current_remainder = [a * current_quotient for a in other.args]
                current_remainder = self.augment(current_remainder, dividend)
                dividend = [x - y for x, y in Polynomial.izip_longest(dividend, current_remainder, fillvalue=0)]
                quotient = tuple(quotient)
                dividend = tuple(dividend)
                return [quotient, dividend]

    def __sub__(self, other):
        self.add_or_subtract(self.args, other.args, 1)
