import collections
import enum
import typing as t

from intcode import Intcode


@enum.unique
class DroidStatus(enum.IntEnum):
    HIT_WALL = 0
    MOVED = 1
    MOVED_AND_FOUND = 2


@enum.unique
class Command(enum.IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class DroidController:

    def __init__(self):
        pass

    @property
    def command(self):
        while True:
            yield Command.NORTH

    def on_output(self, value):
        pass

    def control(self, doid: Intcode):
        doid.run(self.command, self.on_output)


def main():
    droid = Intcode.from_file('input_15.txt')
    controller = DroidController()
    controller.control(droid)


if __name__ == '__main__':
    main()
