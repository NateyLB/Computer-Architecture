"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = []
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # get file from sys.args and populate program
        print(sys.argv)
        print(sys.argv[1])
        file = open(sys.argv[1], "r")
        
        program = []
        for curline in file:
            if curline.startswith('#') or curline == '\n':
                continue
            else:
                split = curline.split(' ', 1)
                split[0] = split[0].strip()
                if len(split) > 1:
                    split[1] = split[1].strip()
                program.append(int(split[0], base=2))
        self.ram = [0] * len(program)
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        print(self.ram, "ram")

    def ram_read(self,MAR):
        """ read value at memory address """
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        """ write value at memory address"""
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def HLT(self):
        """ HALT instruction definition"""
        return 0b00000001

    

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            inst = self.ram_read(self.pc)
            if inst == self.HLT() :
                ## HALT
                running = False
            elif inst == 0b01000111:
                ## PRN print value in giver register
                reg = self.ram_read(self.pc + 1)
                print(self.reg[reg])
                self.pc += 2
            elif inst == 0b10000010:
                ## LDI set register to value
                reg = self.pc + 1
                val = self.pc + 2
                self.reg[self.ram_read(reg)] = self.ram_read(val)
                self.pc += 3
            elif inst == 0b10100010:
                ## MULT regA and regB together, store esults in regA
                regA = self.pc + 1
                regB = self.pc + 2
                self.reg[self.ram_read(regA)] = self.ram_read(regA) *self.ram_read(regB)
                self.pc += 3



