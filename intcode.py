import enum
import io
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


class TraceItem:
    def __init__(self, address):
        self.address = address
        self.instruction = None
        self.mnemonic = None
        self.arguments = []
        self.result = None

    def __str__(self):
        elements = [f'{self.address:05}', self.mnemonic]
        elements.extend(self.arguments)
        if self.result:
            elements.append(f'-->')
            elements.append(self.result)

        return ' '.join(elements)


class Intcode:
    """An Elve Intcode computer."""

    def __init__(self, *instructions, trace_execution=False):
        self.program = instructions
        self.memory = None
        self.ip = 0
        self.trace = None
        self.trace_execution=trace_execution

    @classmethod
    def from_file(cls, path) -> 'Intcode':
        return cls(*[int(c) for c in pathlib.Path(path).read_text().split(',')])

    def next_instruction(self):
        instruction = self.memory[self.ip]

        self.ip += 1
        return instruction

    def __call__(self, *args, **kwargs):
        return self.run(inputs=args)

    def run(self, inputs: t.Iterable[int] = None) -> t.List[int]:
        self.memory = list(self.program)
        self.ip = 0

        input_iter = iter(inputs) if inputs else None
        outputs = []

        opcode = None
        while opcode is not Opcode.EXIT:
            self.trace = TraceItem(self.ip)

            instruction = self.next_instruction()
            self.trace.instruction = instruction

            opcode = Opcode(instruction % 100)
            parameter_modes = instruction // 100

            if opcode is Opcode.EXIT:
                self.trace.mnemonic = 'EXT'

            elif opcode is Opcode.ADD:
                self.trace.mnemonic = 'ADD'
                self._add(parameter_modes)

            elif opcode is Opcode.MULTIPLY:
                self.trace.mnemonic = 'MUL'
                self._multiply(parameter_modes)

            elif opcode is Opcode.INPUT:
                self.trace.mnemonic = 'INP'
                value = next(input_iter)
                self._store(value)

            elif opcode is Opcode.OUTPUT:
                self.trace.mnemonic = 'OUT'
                value = self._load(ParameterMode(parameter_modes))
                outputs.append(value)

            elif opcode is Opcode.JUMP_IF_TRUE:
                self.trace.mnemonic = 'JNZ'
                self._jump_if(True, parameter_modes)

            elif opcode is Opcode.JUMP_IF_FALSE:
                self.trace.mnemonic = 'JZR'
                self._jump_if(False, parameter_modes)

            elif opcode is Opcode.LESS_THAN:
                self.trace.mnemonic = 'LSS'
                self._less_than(parameter_modes)

            elif opcode is Opcode.EQUALS:
                self.trace.mnemonic = 'EQU'
                self._equals(parameter_modes)

            else:
                raise NotImplementedError('unexpected opcode', opcode)

            if self.trace_execution:
                _logger.debug(self.trace)

        return outputs

    def _add(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 + param2)

    def _multiply(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 * param2)

    def _store(self, value: int):
        address = self.next_instruction()
        self.trace.result = f'({address})'
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
            self.trace.arguments.append(str(value))
            return value

        if mode is ParameterMode.POSITION:
            self.trace.arguments.append(f'({value})')
            return self.memory[value]

        raise NotImplementedError('unknown parameter mode', mode)

    def _jump_if(self, condition: bool, parameter_modes: int):
        value, address = self._load_multiple(2, parameter_modes)
        if bool(value) is condition:
            self.ip = address

    def _less_than(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 < param2 else 0
        self._store(value)

    def _equals(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 == param2 else 0
        self._store(value)
