import logging

from solution_05 import Intcode

logging.basicConfig(format='%(asctime)-15s %(levelname)-7s %(message)s', level=logging.INFO)


def memory_after_run(program):
    computer = Intcode(*program)
    computer()
    return computer.memory


def test__run_from_02():
    assert memory_after_run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert memory_after_run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert memory_after_run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert memory_after_run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def test__run():
    assert memory_after_run([1002, 4, 3, 4, 33])[4] == 99
    assert memory_after_run([1101, 100, -1, 4, 0])[4] == 99


def test__part_1():
    output = Intcode.from_file('input_05.txt').run([1])
    assert output == [0, 0, 0, 0, 0, 0, 0, 0, 0, 5821753]


def test__equal_8__position():
    compare_to_8 = Intcode(3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8)
    assert compare_to_8(7) == [0]
    assert compare_to_8(9) == [0]
    assert compare_to_8(8) == [1]


def test__less_than_8__position():
    less_than_8 = Intcode(3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8)
    assert less_than_8(6) == [1]
    assert less_than_8(7) == [1]
    assert less_than_8(8) == [0]
    assert less_than_8(9) == [0]


def test__equal_8__immediate():
    compare_to_8 = Intcode(3, 3, 1108, -1, 8, 3, 4, 3, 99)
    assert compare_to_8(7) == [0]
    assert compare_to_8(9) == [0]
    assert compare_to_8(8) == [1]


def test__less_than_8__immediate():
    less_than_8 = Intcode(3, 3, 1107, -1, 8, 3, 4, 3, 99)
    assert less_than_8(6) == [1]
    assert less_than_8(7) == [1]
    assert less_than_8(8) == [0]
    assert less_than_8(9) == [0]


def jump__position():
    jump = Intcode(3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9)
    assert jump(-1) == [1]
    assert jump(-0) == [0]
    assert jump(1) == [1]


def jump__immediate():
    jump = Intcode(3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1)
    assert jump(-1) == [1]
    assert jump(-0) == [0]
    assert jump(1) == [1]
