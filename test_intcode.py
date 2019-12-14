from intcode import ParameterMode


def test__parameter_mode__from_modes():
    assert ParameterMode.from_modes(0, 0) == 0
    assert ParameterMode.from_modes(0, 1) == 0
    assert ParameterMode.from_modes(10, 0) == 0
    assert ParameterMode.from_modes(10, 1) == 1
    assert ParameterMode.from_modes(1010, 0) == 0
    assert ParameterMode.from_modes(1020, 1) == 2
    assert ParameterMode.from_modes(1010, 2) == 0
    assert ParameterMode.from_modes(1010, 3) == 1
