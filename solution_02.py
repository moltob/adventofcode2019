import enum
import operator
import pathlib
import typing as t


@enum.unique
class Opcode(enum.IntEnum):
    EXIT = 99
    ADD = 1
    MULTIPLY = 2


OPERATIONS = {
    Opcode.ADD.value: operator.add,
    Opcode.MULTIPLY.value: operator.mul,
}


def run(ram: t.List[int]) -> t.List[int]:
    ip = 0

    while (opcode := ram[ip]) != Opcode.EXIT:
        try:
            operation = OPERATIONS[opcode]
        except ValueError:
            print(f'Encountered unknown opcode {opcode} at position {ip}.')
            break

        ram[ram[ip + 3]] = operation(ram[ram[ip + 1]], ram[ram[ip + 2]])
        ip += 4

    print(f'Program state after execution: {ram!r}')
    return ram


def main():
    program = [int(c) for c in pathlib.Path('input_02.txt').read_text().split(',')]

    # restore 1202 state:
    program[1] = 12
    program[2] = 2

    run(program)


if __name__ == '__main__':
    main()
