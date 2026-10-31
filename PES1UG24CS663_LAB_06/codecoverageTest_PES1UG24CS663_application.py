"""Line-coverage tests for bike_share_rental.py."""

import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


def test_ride_cost_valid_paths_and_adjustments():
    assert ride_cost("standard", 45, False, False) == 40
    assert ride_cost("electric", 30, True, False) == 0
    assert ride_cost("cargo", 60, True, True) == 50
    assert ride_cost("standard", 181, False, True) == 255


@pytest.mark.parametrize(
    "bike_type,minutes,message",
    [
        ("tandem", 30, "unknown bike type"),
        ("standard", 0, "invalid duration"),
    ],
)
def test_ride_cost_rejects_invalid_inputs(bike_type, minutes, message):
    with pytest.raises(ValueError, match=message):
        ride_cost(bike_type, minutes, False, False)


def test_dock_status_categories():
    assert dock_status(0, 10) == "empty"
    assert dock_status(10, 10) == "full"
    assert dock_status(2, 10) == "few bikes"
    assert dock_status(8, 10) == "few slots"
    assert dock_status(5, 10) == "available"


@pytest.mark.parametrize(
    "bikes,capacity,message",
    [
        (1, 0, "invalid capacity"),
        (-1, 10, "invalid bike count"),
        (11, 10, "invalid bike count"),
    ],
)
def test_dock_status_rejects_invalid_inputs(bikes, capacity, message):
    with pytest.raises(ValueError, match=message):
        dock_status(bikes, capacity)


def test_unlock_decisions():
    assert can_unlock(500, True, 25) is False
    assert can_unlock(500, False, 15) is False
    assert can_unlock(100, False, 16) is True
    assert can_unlock(50, False, 18) is True
