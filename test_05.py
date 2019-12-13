from solution_05 import Intcode


def memory_after_run(program):
    computer = Intcode(program)
    computer.run()
    return computer.memory


def test__run_from_02():
    assert memory_after_run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert memory_after_run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert memory_after_run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert memory_after_run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def test__run():
    assert memory_after_run([1002, 4, 3, 4, 33])[4] == 99
    assert memory_after_run([1101, 100, -1, 4, 0])[4] == 99
