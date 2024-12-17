import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        text = file.read()

        register_section, program_section = text.split('\n\n')
        registers = register_section.split('\n')
        a = int(registers[0].split(':')[-1])
        b = int(registers[1].split(':')[-1])
        c = int(registers[2].split(':')[-1])

        program = [int(e) for e in program_section.split(':')[-1].split(',')]
        return a, b, c, program


class Computer:
    A = 0
    B = 0
    C = 0
    program = []
    ip = 0
    output = []

    def __init__(self, a, b, c, program):
        self.A = a
        self.B = b
        self.C = c
        self.program = program
        self.ip = 0
        self.output = []

    def reset(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.ip = 0
        self.output = []

    def run_opcode(self, opcode, operand):
        if opcode == 0:
            denominator = 2 ** self.get_combo_operand(operand)
            self.A = self.A // denominator
            self.ip += 2
        elif opcode == 1:
            self.B ^= operand
            self.ip += 2
        elif opcode == 2:
            self.B = self.get_combo_operand(operand) % 8
            self.ip += 2
        elif opcode == 3:
            if self.A == 0:
                self.ip += 2
            elif self.A != 0:
                self.ip = operand
        elif opcode == 4:
            self.B ^= self.C
            self.ip += 2
        elif opcode == 5:
            self.output.append(self.get_combo_operand(operand) % 8)
            self.ip += 2
        elif opcode == 6:
            denominator = 2 ** self.get_combo_operand(operand)
            self.B = self.A // denominator
            self.ip += 2
        elif opcode == 7:
            denominator = 2 ** self.get_combo_operand(operand)
            self.C = self.A // denominator
            self.ip += 2
        else:
            raise ValueError(f"Undefined opcode: {opcode}")

    def run(self):
        self.ip = 0
        self.output = []

        while 0 <= self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            self.run_opcode(opcode, operand)

        return self.output

    def get_combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            raise ValueError("The operand 7 is reserved.")

    def find_register_a(self, idx=0, a=0):
        size = len(self.program)
        if idx == size:
            return a
        for val in range(8):
            if idx == 0 and val == 0:
                continue
            self.reset()
            self.A = a * 8 + val
            expected = self.program[size - idx - 1:]
            output = self.run()
            if output == expected:
                found = self.find_register_a(idx + 1, a * 8 + val)
                if found is not None:
                    return found


def part1(input_file_path: str):
    a, b, c, program = parse_input(input_file_path)
    computer = Computer(a, b, c, program)
    result = computer.run()
    return ",".join(map(str, result))


def part2(input_file_path: str):
    a, b, c, program = parse_input(input_file_path)
    computer = Computer(a, b, c, program)
    return computer.find_register_a()


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/17/example.txt', '4,6,3,5,6,3,5,2,1,0'),
    ('inputs/17/input.txt', '7,0,7,3,4,1,3,0,1')
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/17/input.txt', 156985331222018)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected


def test_scenario_1():
    sut = Computer(0, 0, 9)
    sut.run()
    assert sut.B == 1


def test_scenario_2():
    sut = Computer(10, 0, 0)
    actual = sut.run()
    assert actual == [0, 1, 2]


def test_scenario_3():
    sut = Computer(2024, 0, 0)
    actual = sut.run()
    assert sut.A == 0
    assert actual == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]


def test_scenario_4():
    sut = Computer(0, 29, 0)
    sut.run()
    assert sut.B == 26


def test_scenario_5():
    sut = Computer(0, 2024, 43690)
    actual = sut.run()
    assert sut.B == 44354


def test_get_combo_operands():
    sut = Computer(1, 2, 3)

    assert sut.get_combo_operand(0) == 0
    assert sut.get_combo_operand(1) == 1
    assert sut.get_combo_operand(2) == 2
    assert sut.get_combo_operand(3) == 3
    assert sut.get_combo_operand(4) == sut.A
    assert sut.get_combo_operand(5) == sut.B
    assert sut.get_combo_operand(6) == sut.C
    with pytest.raises(ValueError, match="The operand 7 is reserved."):
        sut.get_combo_operand(7)
