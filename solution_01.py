import pathlib


def compute_fuel(mass: int) -> int:
    return mass // 3 - 2


def compute_total_fuel(mass: int) -> int:
    fuel = compute_fuel(mass)
    if fuel > 0:
        return fuel + compute_total_fuel(fuel)
    return 0


def compute_total_fuel_iterative(mass: int) -> int:
    fuel = 0

    while (mass := compute_fuel(mass)) > 0:
        fuel += mass

    return fuel


def main():
    masses = [int(m) for m in pathlib.Path('input_01.txt').read_text().splitlines(keepends=False)]

    print('Fuel without fuel mass', sum(compute_fuel(m) for m in masses))
    print('Fuel with fuel mass', sum(compute_total_fuel(m) for m in masses))


if __name__ == '__main__':
    main()
