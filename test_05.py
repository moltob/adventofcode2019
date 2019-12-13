from solution_05 import Intcode


def test__run_from_02():
    assert Intcode([1, 0, 0, 0, 99]).run().memory == [2, 0, 0, 0, 99]
    assert Intcode([1, 0, 0, 0, 99]).run().memory == [2, 0, 0, 0, 99]
    assert Intcode([2, 3, 0, 3, 99]).run().memory == [2, 3, 0, 6, 99]
    assert Intcode([2, 4, 4, 5, 99, 0]).run().memory == [2, 4, 4, 5, 99, 9801]
    assert Intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]).run().memory == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def test__run():
    assert Intcode([1002, 4, 3, 4, 33]).run().memory[4] == 99
