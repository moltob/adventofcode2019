from solution_01 import compute_fuel, compute_total_fuel, compute_total_fuel_iterative


def test__compute_fuel():
    assert compute_fuel(12) == 2
    assert compute_fuel(14) == 2
    assert compute_fuel(1969) == 654
    assert compute_fuel(100756) == 33583


def test__compute_total_fuel():
    assert compute_total_fuel(14) == 2
    assert compute_total_fuel(1969) == 966
    assert compute_total_fuel(100756) == 50346


def test__compute_total_fuel_iterative():
    assert compute_total_fuel_iterative(14) == 2
    assert compute_total_fuel_iterative(1969) == 966
    assert compute_total_fuel_iterative(100756) == 50346
