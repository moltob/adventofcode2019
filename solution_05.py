import logging

import colorama
import daiquiri

from intcode import Intcode


def main():
    colorama.init()
    daiquiri.setup('DEBUG')

    diagnostic = Intcode.from_file('input_05.txt')
    print('air conditioner:', diagnostic(1))
    diagnostic.trace_execution = True
    print('thermal radiator controller:', diagnostic(5))


if __name__ == '__main__':
    main()
