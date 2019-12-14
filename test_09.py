from intcode import Intcode


def test__copy():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert Intcode(*program)() == program


def test__16_digits_output():
    outputs = Intcode(1102, 34915192, 34915192, 7, 4, 7, 99, 0)()
    assert len(outputs) == 1
    assert len(str(outputs[0])) == 16


def test__large_output():
    outputs = Intcode(104, 1125899906842624, 99)()
    assert outputs == [1125899906842624]


def test__part_1():
    boost = Intcode.from_file('input_09.txt')
    assert boost(1) == [2932210790]
