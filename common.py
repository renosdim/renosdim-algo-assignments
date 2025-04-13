def binary_to_decimal(binary):
    if isinstance(binary, str):
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        return decimal
    else:
        return int(binary, 2)

def decimal_to_binary(decimal):
    binary = bin(decimal)[2:]
    return binary

def decimal_to_balanced_ternary(decimal):
    if decimal == 0:
        return "0"
    
    digits = []
    while decimal != 0:
        remainder = decimal % 3
        
        if remainder == 2:
            remainder = -1
            decimal += 3
        elif remainder == -2:
            remainder = 1
            decimal -= 3
            
        digits.append(remainder)
        decimal //= 3
    
    balanced_ternary = ""
    for digit in reversed(digits):
        if digit == -1:
            balanced_ternary += "-"
        elif digit == 1:
            balanced_ternary += "+"
        else:
            balanced_ternary += str(digit)
    
    return balanced_ternary

def binary_to_balanced_ternary(binary):
    decimal = binary_to_decimal(binary)
    return decimal_to_balanced_ternary(decimal)

def balanced_ternary_to_binary(s):
    result = []
    for char in s:
        if char == '0':
            result.append('1')
        elif char in ['+', '-']:
            result.append('0')
        else:
            result.append(char)
    
    return ''.join(result)

def binary_to_index(binary_str):
    indices = []
    reversed_str = binary_str[::-1]

    for i, bit in enumerate(reversed_str):
        if bit == '1':
            indices.append(str(i))

    return ''.join(sorted(indices, reverse=True))

def index_to_decimal(index_str, s, t):
    total_length = s + t
    binary = ['0'] * total_length
    
    for position in index_str:
        pos = int(position)
        binary[total_length - 1 - pos] = '1'
        
    return int(''.join(binary), 2)

def generate_total_binaries(s, t):
    result = []

    def backtrack(current, zeros_left, ones_left):
        if zeros_left == 0 and ones_left == 0:
            result.append(''.join(current))
            return

        if zeros_left > 0:
            current.append('0')
            backtrack(current, zeros_left - 1, ones_left)
            current.pop()

        if ones_left > 0:
            current.append('1')
            backtrack(current, zeros_left, ones_left - 1)
            current.pop()

    backtrack([], s, t)
    return result