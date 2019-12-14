import enum
import pathlib
import typing as t


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
    ADJUST_RELATIVE_BASE = 9


@enum.unique
class ParameterMode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class TraceItem:
    def __init__(self, address):
        self.address: int = address
        self.opcode: Opcode = Opcode.EXIT
        self.parameter_mode = 0
        self.mnemonic: str = ''
        self.arguments: t.List[str] = []
        self.result: t.Optional[str] = None

    def __str__(self):
        elements = [
            f'{self.address:05}',
            f'{self.parameter_mode:03}|{self.opcode.value:02}',
            self.mnemonic,
            ','.join(self.arguments)
        ]
        if self.result:
            elements.append(f'-->')
            elements.append(self.result)

        return ' '.join(elements)


class Intcode:
    """An Elve Intcode computer."""

    def __init__(self, *instructions):
        self.program = instructions
        self.memory = None
        self.ip = 0
        self.relative_base = 0
        self.trace = []
        self._trace_line = None

    @classmethod
    def from_file(cls, path) -> 'Intcode':
        return cls(*[int(c) for c in pathlib.Path(path).read_text().split(',')])

    def print_trace(self):
        print('======================================')
        print('ADDR  INSTR  COMMAND')
        print('======================================')
        print('\n'.join(self.trace))
        print('======================================')

    def next_instruction(self):
        instruction = self.memory[self.ip]

        self.ip += 1
        return instruction

    def __call__(self, *args, **kwargs):
        return self.run(inputs=args)

    def run(self, inputs: t.Iterable[int] = None) -> t.List[int]:
        self.memory = list(self.program)
        self.ip = 0
        self.relative_base = 0
        self.trace = []

        input_iter = iter(inputs) if inputs else None
        outputs = []

        opcode = None
        while opcode is not Opcode.EXIT:
            self._trace_line = TraceItem(self.ip)

            instruction = self.next_instruction()

            opcode = Opcode(instruction % 100)
            parameter_modes = instruction // 100
            self._trace_line.opcode = opcode
            self._trace_line.parameter_mode = parameter_modes

            if opcode is Opcode.EXIT:
                self._trace_line.mnemonic = 'EXT'

            elif opcode is Opcode.ADD:
                self._trace_line.mnemonic = 'ADD'
                self._add(parameter_modes)

            elif opcode is Opcode.MULTIPLY:
                self._trace_line.mnemonic = 'MUL'
                self._multiply(parameter_modes)

            elif opcode is Opcode.INPUT:
                self._trace_line.mnemonic = 'INP'
                value = next(input_iter)
                self._store(value)

            elif opcode is Opcode.OUTPUT:
                self._trace_line.mnemonic = 'OUT'
                value = self._load(ParameterMode(parameter_modes))
                outputs.append(value)

            elif opcode is Opcode.JUMP_IF_TRUE:
                self._trace_line.mnemonic = 'JNZ'
                self._jump_if(True, parameter_modes)

            elif opcode is Opcode.JUMP_IF_FALSE:
                self._trace_line.mnemonic = 'JZR'
                self._jump_if(False, parameter_modes)

            elif opcode is Opcode.LESS_THAN:
                self._trace_line.mnemonic = 'LSS'
                self._less_than(parameter_modes)

            elif opcode is Opcode.EQUALS:
                self._trace_line.mnemonic = 'EQU'
                self._equals(parameter_modes)

            elif opcode is Opcode.ADJUST_RELATIVE_BASE:
                self._trace_line.mnemonic = 'ARB'
                self._adjust_relative_base(parameter_modes)

            else:
                raise NotImplementedError('unexpected opcode', opcode)

            self.trace.append(str(self._trace_line))

        return outputs

    def _add(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 + param2)

    def _multiply(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 * param2)

    def _store(self, value: int):
        address = self.next_instruction()
        self._trace_line.result = f'({address})'
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
            self._trace_line.arguments.append(str(value))
            return value

        if mode is ParameterMode.POSITION:
            self._trace_line.arguments.append(f'({value})')
            return self.memory[value]

        if mode is ParameterMode.RELATIVE:
            self._trace_line.arguments.append(f'/{value}/')
            return self.memory[self.relative_base + value]

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

    def _adjust_relative_base(self, parameter_modes):
        adjustment = self._load(ParameterMode(parameter_modes))
        self.relative_base += adjustment
