from intcode import Intcode


def main():
    diagnostic = Intcode.from_file('input_05.txt')
    print('air conditioner:', diagnostic(1))
    print('thermal radiator controller:', diagnostic(5))


if __name__ == '__main__':
    main()
