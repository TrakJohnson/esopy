# coding=utf-8
"""Brainfuck Interpreter"""

tape = [0] * 256
index = 0
with open("code") as raw_code:
    code = raw_code.read()


def parse_code(start=0, end=len(code)):
    global index, tape, code
    # Handling loops
    loops_temp = []
    loops = {}
    for char_index, char in enumerate(code):
        if char == '[':
            loops_temp.append(char_index)
        if char == ']':
            opening = loops_temp.pop()
            loops[opening] = char_index
    if loops_temp:
        raise ValueError("Unmatched brackets")
    code_index = start
    # Parse code
    while code_index < end:
        char_ = code[code_index]
        if index < 0 or index > 1024:
            raise IndexError
        if char_ == '>':
            index += 1
        if char_ == '<':
            index -= 1
        if char_ == '+':
            tape[index] += 1
        if char_ == '-':
            tape[index] -= 1
        if char_ == '.':
            print(chr(tape[index]))
        if char_ == ',':
            tape[index] = ord(input()[0])
        if code_index in loops:  # if char == '['
            while tape[index]:
                parse_code(start=code_index+1, end=loops[code_index])
            code_index = loops[code_index]
        code_index += 1

if __name__ == '__main__':
    parse_code()
