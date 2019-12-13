import enum
import logging
import pathlib
import typing as t

_logger = logging.getLogger(__name__)


@enum.unique
class Opcode(enum.IntEnum):
    EXIT = 99
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8


@enum.unique
class ParameterMode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class Intcode:
    """An Elve Intcode computer."""

    def __init__(self, *instructions):
        self.program = instructions
        self.memory = None
        self.ip = 0

    @classmethod
    def from_file(cls, path) -> 'Intcode':
        _logger.debug(f'Loading program from file "{path}".')
        return cls(*[int(c) for c in pathlib.Path(path).read_text().split(',')])

    def next_instruction(self):
        instruction = self.memory[self.ip]
        _logger.debug(f'Read instruction code {instruction} at {self.ip}.')

        self.ip += 1
        return instruction

    def __call__(self, *args, **kwargs):
        return self.run(inputs=args)

    def run(self, inputs: t.Iterable[int] = None) -> t.List[int]:
        _logger.info('Starting program execution.')
        self.memory = list(self.program)
        self.ip = 0
        outputs = []

        input_iter = iter(inputs) if inputs else None

        while True:
            instruction = self.next_instruction()
            opcode = Opcode(instruction % 100)
            parameter_modes = instruction // 100

            if opcode is Opcode.EXIT:
                _logger.info('Exiting normally.')
                break

            if opcode is Opcode.ADD:
                self._add(parameter_modes)

            elif opcode is Opcode.MULTIPLY:
                self._multiply(parameter_modes)

            elif opcode is Opcode.INPUT:
                value = next(input_iter)
                _logger.info(f'Passing input {value}.')
                self._store(value)

            elif opcode is Opcode.OUTPUT:
                value = self._load(ParameterMode(parameter_modes))
                _logger.info(f'Output {value}.')
                outputs.append(value)

            elif opcode is Opcode.JUMP_IF_TRUE:
                self._jump_if(True, parameter_modes)

            elif opcode is Opcode.JUMP_IF_FALSE:
                self._jump_if(False, parameter_modes)

            elif opcode is Opcode.LESS_THAN:
                self._less_than(parameter_modes)

            elif opcode is Opcode.EQUALS:
                self._equals(parameter_modes)

            else:
                raise NotImplementedError('unexpected opcode', opcode)

        return outputs

    def _add(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        _logger.info(f'Adding {param1} and {param2}.')
        self._store(param1 + param2)

    def _multiply(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        _logger.info(f'Multiplying {param1} and {param2}.')
        self._store(param1 * param2)

    def _store(self, value: int):
        address = self.next_instruction()
        _logger.info(f'Storing {value} at {address}.')
        self.memory[address] = value

    def _load_multiple(self, number: int, parameter_modes: int) -> t.List[int]:
        values = []

        while number:
            mode = ParameterMode(parameter_modes % 10)
            parameter_modes //= 10
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

    def _jump_if(self, condition: bool, parameter_modes: int):
        value, address = self._load_multiple(2, parameter_modes)
        if bool(value) is condition:
            _logger.info(f'Jumping to {address} because {value} is {condition}.')
            self.ip = address
        else:
            _logger.info(f'Not jumping to {address} because {value} is {condition}.')

    def _less_than(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 < param2 else 0
        self._store(value)

    def _equals(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 == param2 else 0
        self._store(value)