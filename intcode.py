import collections
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

    @classmethod
    def from_modes(cls, modes, pos):
        return cls(modes // pow(10, pos) % 10)


class TraceItem:
    def __init__(self, address, relative_base):
        self.address: int = address
        self.relative_base = relative_base
        self.opcode: Opcode = Opcode.EXIT
        self.parameter_mode = 0
        self.mnemonic: str = ''
        self.arguments: t.List[str] = []
        self.result: t.Optional[str] = None

    def __str__(self):
        elements = [
            f'{self.address:05}',
            f'/{self.relative_base:08}/',
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
        self.program = list(instructions)
        self._memory = collections.defaultdict(int)
        self.ip = 0
        self.relative_base = 0
        self.trace = []
        self._trace_line = None
        self.stack_trace_on_error = True

    @classmethod
    def from_file(cls, path) -> 'Intcode':
        return cls(*[int(c) for c in pathlib.Path(path).read_text().split(',')])

    @property
    def memory(self) -> t.List[int]:
        if not self._memory:
            return []

        max_index = max(self._memory.keys())
        return [self._memory[i] for i in range(max_index + 1)]

    def print_trace(self):
        print('=============================================')
        print('ADDR  RELBASE    INSTR  COMMAND')
        print('=============================================')
        print('\n'.join(self.trace))
        print('=============================================')

    def next_instruction(self):
        instruction = self._memory[self.ip]

        self.ip += 1
        return instruction

    def __call__(self, *args, **kwargs):
        return self.run(inputs=args)

    def run(
            self, inputs: t.Iterable[int] = None,
            on_output: t.Callable[[int], None] = None
    ) -> t.List[int]:
        self._memory.clear()
        self._memory.update({i: v for i, v in enumerate(self.program)})

        self.ip = 0
        self.relative_base = 0
        self.trace = []

        input_iter = iter(inputs) if inputs else None
        outputs = []

        opcode = None
        while opcode is not Opcode.EXIT:
            self._trace_line = TraceItem(self.ip, self.relative_base)

            instruction = self.next_instruction()

            opcode = Opcode(instruction % 100)
            parameter_modes = instruction // 100
            self._trace_line.opcode = opcode
            self._trace_line.parameter_mode = parameter_modes

            try:

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
                    self._store(value, ParameterMode.from_modes(parameter_modes, 0))

                elif opcode is Opcode.OUTPUT:
                    self._trace_line.mnemonic = 'OUT'
                    value = self._load(ParameterMode(parameter_modes))
                    outputs.append(value)
                    if on_output:
                        on_output(value)

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
            except:
                if self.stack_trace_on_error:
                    print(f'Program execution failed:')
                    self.print_trace()
                    print(f'{self._trace_line} <-- FAILED')
                raise

        return outputs

    def _add(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 + param2, ParameterMode.from_modes(parameter_modes, 2))

    def _multiply(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        self._store(param1 * param2, ParameterMode.from_modes(parameter_modes, 2))

    def _store(self, value: int, mode: ParameterMode):
        address = self.next_instruction()

        if mode is ParameterMode.POSITION:
            entry = f'({address})={value}'
        elif mode is ParameterMode.RELATIVE:
            entry = f'/{address}/={value}'
            address = self.relative_base + address
        else:
            raise NotImplementedError('unsupported storage mode', mode)

        self._trace_line.result = entry
        self._memory[address] = value

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
            return self._memory[value]

        if mode is ParameterMode.RELATIVE:
            self._trace_line.arguments.append(f'/{value}/')
            return self._memory[self.relative_base + value]

        raise NotImplementedError('unknown parameter mode', mode)

    def _jump_if(self, condition: bool, parameter_modes: int):
        value, address = self._load_multiple(2, parameter_modes)
        if bool(value) is condition:
            self.ip = address

    def _less_than(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 < param2 else 0
        self._store(value, ParameterMode.from_modes(parameter_modes, 2))

    def _equals(self, parameter_modes):
        param1, param2 = self._load_multiple(2, parameter_modes)
        value = 1 if param1 == param2 else 0
        self._store(value, ParameterMode.from_modes(parameter_modes, 2))

    def _adjust_relative_base(self, parameter_modes):
        adjustment = self._load(ParameterMode(parameter_modes))
        self.relative_base += adjustment
