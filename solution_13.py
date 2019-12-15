import collections
import enum
import typing as t

from intcode import Intcode


@enum.unique
class TileId(enum.IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HPADDLE = 3
    BALL = 4


Vector = collections.namedtuple('Vector', 'x y')


def track_screen(control_codes: t.Iterable[int], tracked_tile_id: TileId) -> t.Set[Vector]:
    coordinates = set()
    control_code_iter = iter(control_codes)

    try:
        while True:
            vector = next(control_code_iter), next(control_code_iter)
            tile_id = TileId(next(control_code_iter))

            if tile_id is tracked_tile_id:
                coordinates.add(vector)
            else:
                try:
                    coordinates.remove(vector)
                except KeyError:
                    pass
    except StopIteration:
        return coordinates


def main():
    arcade = Intcode.from_file('input_13.txt')
    screen_control_sequences = arcade()
    print('number of block tiles:', len(track_screen(screen_control_sequences, TileId.BLOCK)))


if __name__ == '__main__':
    main()
