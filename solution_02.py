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
        except ValueError:
            print(f'Encountered unknown opcode {opcode} at position {ip}.')
            break

        ram[ram[ip + 3]] = operation(ram[ram[ip + 1]], ram[ram[ip + 2]])
        ip += 4

    print(f'Program state after execution: {ram!r}')
    return ram


def run_with(program: t.List[int], noun: int, verb: int) -> int:
    ram = copy.deepcopy(program)
    ram[1:3] = noun, verb
    run(ram)
    return ram[0]


def brute_force(program: t.List[int], output: int) -> t.Tuple[int, int]:
    for noun in range(100):
        for verb in range(100):
            if run_with(program, noun, verb) == output:
                print(f'program({noun}, {verb})={output}')
                return noun, verb

    print(f'No combination found to produce {output}.')
    return -1, -1


def main():
    program = [int(c) for c in pathlib.Path('input_02.txt').read_text().split(',')]

    print('Result with 1202 state:', run_with(program, 12, 2))

    noun, verb = brute_force(program, 19690720)
    print('Result code:', 100 * noun + verb)


if __name__ == '__main__':
    main()
