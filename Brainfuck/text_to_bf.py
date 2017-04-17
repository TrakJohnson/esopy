"""
Converts text to a bf program that will output it
Very inefficient for now.
"""

import math


class Converter:
    def __init__(self, str_in):
        self.all_codes = [ord(c) for c in str_in]
        self.result_code = ''

    def convert(self):
        min_char_code = min(self.all_codes)
        while True:
            test_values = self.find_closest_multiples(min_char_code)
            if 1 in test_values:
                min_char_code -= 1
            else:
                break
        self.result_code += '+' * 10 + '[->'
        for letter_code in self.all_codes:
            self.result_code += '>' + '+' * (letter_code // 10)
        self.result_code += '[<]<]>'
        for letter_code in self.all_codes:
            self.result_code += '>' + '+' * (letter_code % 10)
        self.result_code += '[<]>[.>]'
        print(self.result_code)

    @staticmethod
    def find_closest_multiples(n):
        """
        finds closes multiples of a number
        ex: 2400 -> (48, 50)
        ex: 37   -> (37, 1)  # prime number 
        """
        c = math.ceil(math.sqrt(n))
        while True:
            if n % c == 0:
                return c, n // c
            c += 1


if __name__ == '__main__':
    c = Converter('Hello World')
    print(c)
