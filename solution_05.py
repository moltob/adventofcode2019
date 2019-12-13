import collections
import copy
import enum
import operator
import os
import pathlib
import typing as t


@enum.unique
class Opcode(enum.IntEnum):
    EXIT = 99
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4


@enum.unique
class ParameterMode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class Intcode:
    """An Elve Intcode computer."""

    def __init__(self, program: t.List[int]):
        self.memory = list(program)
        self.ip = 0

    @classmethod
    def from_file(cls, path) -> 'Intcode':
        return cls([int(c) for c in pathlib.Path(path).read_text().split(',')])

    def next_instruction(self):
        instruction = self.memory[self.ip]
        self.ip += 1
        return instruction

    def run(
            self,
            *,
            inputs: t.Optional[t.List[int]] = None,
            outputs: t.Optional[t.List[int]] = None
    ) -> 'Intcode':
        inputp = 0

        while True:
            instruction = self.next_instruction()
            opcode = Opcode(instruction % 100)
            modes_code = instruction // 100

            if opcode is Opcode.EXIT:
                break

            if opcode is Opcode.ADD:
                param1, param2 = self._load_multiple(2, modes_code)
                self._store(param1 + param2)

            elif opcode is Opcode.MULTIPLY:
                param1, param2 = self._load_multiple(2, modes_code)
                self._store(param1 * param2)

            elif opcode is Opcode.INPUT:
                if inputs is None:
                    value = int(input('Please enter a value: '))
                else:
                    value = inputs[inputp]
                    inputp += 1
                self._store(value)

            elif opcode is Opcode.OUTPUT:
                value = self._load(ParameterMode(modes_code))
                if outputs is None:
                    print(value)
                else:
                    outputs.append(value)

            else:
                raise NotImplementedError('unexpected opcode', opcode)

        # to simplify test assertions:
        return self

    def _store(self, value: int):
        self.memory[self.next_instruction()] = value

    def _load_multiple(self, number: int, modes_code: int) -> t.List[int]:
        values = []

        while number:
            mode = ParameterMode(modes_code % 10)
            modes_code //= 10
            number -= 1
            values.append(self._load(mode))

        return values

    def _load(self, mode: ParameterMode) -> int:
        value = self.next_instruction()

        if mode is ParameterMode.IMMEDIATE:
            return value

        if mode is ParameterMode.POSITION:
            return self.memory[value]

        raise NotImplementedError('unknown parameter mode', mode)


def main():
    outputs = []
    Intcode.from_file('input_05.txt').run(inputs=[1], outputs=outputs)
    print(outputs)


if __name__ == '__main__':
    main()
