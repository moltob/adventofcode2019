import copy
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
        except KeyError:
            print(f'Encountered unknown opcode {opcode} at position {ip}.')
            break

        ram[ram[ip + 3]] = operation(ram[ram[ip + 1]], ram[ram[ip + 2]])
        ip += 4

    return ram


def main():
    pass


if __name__ == '__main__':
    main()
