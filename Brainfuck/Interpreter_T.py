"""
brainf. interpreter in python

(Program Start)	
    char array[infinitely large size] = {0};
    char *ptr=array;

/-----------------------------------\    
|   Bf command |    C command       | 
|-----------------------------------|
|      >	   |    ++ptr;          | 
|      <	   |    --ptr;          |
|      +	   |    ++*ptr;         |
|      -	   |    --*ptr;         |
|      .	   |    putchar(*ptr);  |
|      ,	   |    *ptr=getchar(); |
|      [	   |    while (*ptr) {  |
|      ]	   |    }               |
\-----------------------------------/
"""

import sys


class ArgumentConflict(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Parser:
    def __init__(self, pointer=0, tape=None, tape_infinite_expansion=False,
                 tape_length=None, allow_other_chars=True):
        """
        Main brainf parser
        :param pointer: initial pointer position on the tape
        :param tape: you can pass a custom tape (list with numbers >= 0)
        :param tape_infinite_expansion: if True, tape will will expand infinitely to the right 
        :param allow_other_chars: If false, will raise an error if it encounters other chars
        """
        self.pointer = pointer
        self.infinite_expansion = tape_infinite_expansion
        if tape_length and tape_infinite_expansion:
            raise ArgumentConflict("Cannot specify tape length if infinite expansion is enabled")
        self.tape_length = tape_length if tape_length else 3*(10**4)
        self.allow_other_chars = allow_other_chars  # TODO: implement that
        self.commands = {
            '>': self.increment_pointer,
            '<': self.decrement_pointer,
            '+': self.increment_value,
            '-': self.decrement_value,
            ',': self.read_input,
            '.': self.write_output,
            '[': None,  # we don't run
            ']': None,  # any of these
        }

        if tape:
            self.tape = tape
        else:
            self.tape = [0 for _ in range(self.tape_length)]
            
    def increment_pointer(self):
        """equivalent of >"""
        if not self.infinite_expansion:
            if self.pointer > len(self.tape):
                raise ValueError('Segmentation fault')
        self.pointer += 1
    
    def decrement_pointer(self):
        """equivalent of <"""
        if self.pointer < 0:
            raise ValueError('Segmentation fault')
        self.pointer -= 1
    
    def increment_value(self):
        """equivalent of +"""
        if self.tape[self.pointer] == 256:
            raise ValueError('Cannot store values > 256')
        else:
            self.tape[self.pointer] += 1
    
    def decrement_value(self):
        """equivalent of -"""
        if self.tape[self.pointer] == 0:
            raise ValueError('Cannot store negative values')
        else:
            self.tape[self.pointer] -= 1

    def read_input(self):
        """equivalent of ,"""
        c = ord(sys.stdin.read(1))
        if c != 26:
            self.tape[self.pointer] = c

    def write_output(self):
        """equivalent of ."""
        sys.stdout.write(chr(self.tape[self.pointer]))

    def parse(self, code):
        """code is a string of .. code"""
        code = ''.join([i for i in code if i in self.commands])
        opening_brackets = []
        code_index = 0
        while code_index < len(code):
            # TODO: check the validity of the input (matched brackets)
            if code[code_index] == '[':
                opening_brackets.append(code_index)
            elif code[code_index] == ']':
                curr_opening_bracket = opening_brackets[-1]
                if self.tape[self.pointer] == 0:
                    opening_brackets.pop()
                else:
                    code_index = curr_opening_bracket  # it will be incremented at the end of the loop anyways
            else:
                self.commands[code[code_index]]()
            code_index += 1

if __name__ == '__main__':
    p = Parser()
    with open('fib.b') as f:
        p.parse(f.read())
