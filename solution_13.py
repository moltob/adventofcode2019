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


@enum.unique
class JoystickPosition(enum.IntEnum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


class Player:

    def __init__(self):
        self.score = 0
        self.game = None

        self._last_output = [0, 0, 0]
        self._last_output_index = 0

    @property
    def joystick(self):
        while True:
            print('Input requested.')
            yield JoystickPosition.NEUTRAL

    def on_output(self, value):
        self._last_output[self._last_output_index] = value
        self._last_output_index += 1

        if self._last_output_index == 3:
            self._on_screen_instruction(*self._last_output)
            self._last_output_index = 0

    def play(self, game: Intcode):
        self.game = game
        self._last_output_index = 0
        game.run(self.joystick, self.on_output)

    def _on_screen_instruction(self, x, y, code):
        if (x, y) == (-1, 0):
            self.score = code
            print(f'New score: {self.score}')
        else:
            self._on_tile(Vector(x, y), TileId(code))

    def _on_tile(self, vector, tile_id):
        print(vector, tile_id.name)


def main():
    arcade = Intcode.from_file('input_13.txt')
    screen_control_sequences = arcade()
    print('number of block tiles:', len(track_screen(screen_control_sequences, TileId.BLOCK)))

    arcade.program[0] = 2
    player = Player()
    player.play(arcade)


if __name__ == '__main__':
    main()
