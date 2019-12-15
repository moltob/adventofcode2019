import collections
import enum
import math
import typing as t

from intcode import Intcode


@enum.unique
class Output(enum.IntEnum):
    HIT_WALL = 0
    MOVED = 1
    MOVED_AND_FOUND = 2


@enum.unique
class Command(enum.IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


Vector = collections.namedtuple('Vector', 'x y')


class HitWallError(Exception):
    """Droid hit a wall."""


class FoundGoal(Exception):
    """Goal found."""


class DroidController:

    def __init__(self):
        self.path: t.List[Vector] = [Vector(0, 0)]
        self.commands = None

    @property
    def position(self):
        return self.path[-1]

    def position_after_move(self, command: Command):
        x, y = self.position
        if command is Command.NORTH:
            y += 1
        elif command is Command.SOUTH:
            y -= 1
        elif command is Command.WEST:
            x -= 1
        elif command is Command.EAST:
            x += 1
        else:
            raise NotImplementedError('unexpected command', command)
        return Vector(x, y)

    def on_input(self):
        for command in self.commands:
            self.path.append(self.position_after_move(command))
            yield command

    def on_output(self, value):
        output = Output(value)

        if output is Output.HIT_WALL:
            raise HitWallError()

        elif output is Output.MOVED_AND_FOUND:
            distance = len(self.path) - 1

            print(f'Found goal at {self.position} after {distance} steps.')
            raise FoundGoal()

    def control(self, doid: Intcode, commands: t.Iterable[Command]):
        self.commands = commands
        doid.run(self.on_input(), self.on_output)


positions = dict()

x_min = 0
x_max = 0
y_min = 0
y_max = 0


def find_shortest_path_length(commands, droid):
    global x_min, x_max, y_min, y_max

    controller = DroidController()

    try:
        controller.control(droid, commands)

    except HitWallError:
        positions[controller.position] = '#'
        return math.inf

    except FoundGoal:
        print(f'*** FOUND at {controller.position} ***')
        positions[controller.position] = '*'
        return len(controller.path)

    except StopIteration:
        # ran out of commands, try next direction from here:
        positions[controller.position] = '.'

        distance = math.inf
        for command in (Command.NORTH, Command.EAST, Command.SOUTH, Command.WEST):
            next_position = controller.position_after_move(command)
            if next_position not in controller.path:
                positions[next_position] = '?'
                x_min = min(next_position.x, x_min)
                x_max = max(next_position.x, x_max)
                y_min = min(next_position.y, y_min)
                y_max = max(next_position.y, y_max)
                distance = min(distance, find_shortest_path_length(commands + [command], droid))
        return distance

    finally:
        print_map()


def print_map():
    for y in range(y_max, y_min - 1, -1):
        row = ''
        for x in range(x_min, x_max + 1):
            if x == y == 0:
                row += '+'
            else:
                tile = positions.get(Vector(x, y), ' ')
                row += tile
        print(row)

    print('------------------------------------')


def main():
    droid = Intcode.from_file('input_15.txt')
    droid.stack_trace_on_error = False
    print('Shortest path length:', find_shortest_path_length([], droid))


if __name__ == '__main__':
    main()
