from intcode import Intcode


def main():
    boost = Intcode.from_file('input_09.txt')
    print('BOOST keycode:', boost(1))
    print('BOOST coordinates of the distress signal:', boost(2))
    # boost.print_trace()


if __name__ == '__main__':
    main()
