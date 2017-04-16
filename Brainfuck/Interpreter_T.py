"""
brainf. interpreter in python

(Program Start)	
    char array[infinitely large size] = {0};
    char *ptr=array;

/----------------------------------\    
| Bf command || C command          | 
|----------------------------------|
|      >	   |    ++ptr;          | 
|      <	   |    --ptr;          |
|      +	   |    ++*ptr;         |
|      -	   |    --*ptr;         |
|      .	   |    putchar(*ptr);  |
|      ,	   |    *ptr=getchar(); |
|      [	   |    while (*ptr) {  |
|      ]	   |    }               |
\---------------------------------/
"""

import sys


class Parser:
    def __init__(self, pointer=0, tape=None, tape_infinite_expansion=False, allow_other_chars=True):
        self.pointer = pointer
        self.infinite_expansion = tape_infinite_expansion
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
            self.tape = [0 for i in range(3*(10**4))]
            
    def increment_pointer(self):
        """equivalent of >"""
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

    def stop_loop(self): pass

    def parse(self, code):
        """code is a string of .. code"""
        code = ''.join([i for i in code if i in self.commands])
        opening_brackets = []
        code_index = 0
        while code_index < len(code):
            # TODO: check the validity of the input
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
    p.parse("""
        ++++++
        >           THIS IS WHERE THE INDEX IS
        +>+<<       INITIAL SETUP (depth;1; 1; 0)
        [>>         OPEN MAIN LOOP
        [->+<]      0; first; 0; second
        <[->+<]     0; 0; first; second
        >>[-<+<+>>] 0; second; third; 0
        <<< -]
    """)



    # """"
    #         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #         >           THIS IS WHERE THE INDEX IS
    #         +>+<<       INITIAL SETUP (depth;1; 1; 0)
    #         [>>         OPEN MAIN LOOP
    #         [->+<]      0; first; 0; second
    #         <[->+<]     0; 0; first; second
    #         >>[-<+<+>>] 0; second; third; 0
    #         <<< -]
    #     """


