"""
Light-weight functions to convert from Roman-Numerals to ints,
and vice-versa.
"""

import string

factor_list = [1000, 500, 100, 50, 10, 5, 1]
roman_equiv = {1000: 'M', 500: 'D', 100: 'C', 50: 'L', 10: 'X', 5: 'V', 1: 'I'}

def IToRoman(num):
    roman = ""
    remainder = num

    factor_index = 0
    for f in factor_list:
        factor_up = (f != 1000 and factor_list[factor_index - 1]) or None
        factor_down = (f != 1 and factor_list[factor_index + 1]) or None
        dividend = remainder / f
        remainder = remainder % f
        if factor_up and dividend == 4:
            roman = roman + roman_equiv[f] + roman_equiv[factor_up]
        elif factor_down and dividend == 1 and remainder / factor_down == 4:
            roman = roman + roman_equiv[factor_down] + roman_equiv[factor_up]
            remainder = remainder % factor_down
        else:
            roman = roman + roman_equiv[f]*dividend
        factor_index = factor_index + 1

    return roman


