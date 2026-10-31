"""Branch-coverage tests for bike_share_rental.py."""

import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


@pytest.mark.parametrize(
    "bike_type,minutes,subscriber,peak,expected",
    [
        ("standard", 45, False, False, 40),
        ("electric", 30, True, False, 0),
        ("standard", 30, True, True, 0),
        ("cargo", 60, True, True, 50),
        ("standard", 30, False, True, 35),
        ("standard", 30, False, False, 20),
        ("electric", 181, False, False, 345),
        ("standard", 180, False, False, 120),
    ],
)
def test_ride_cost_branches(bike_type, minutes, subscriber, peak, expected):
    assert ride_cost(bike_type, minutes, subscriber, peak) == expected


@pytest.mark.parametrize(
    "bike_type,minutes,message",
    [
        ("unicycle", 30, "unknown bike type"),
        ("standard", -1, "invalid duration"),
    ],
)
def test_ride_cost_validation_branches(bike_type, minutes, message):
    with pytest.raises(ValueError, match=message):
        ride_cost(bike_type, minutes, False, False)


@pytest.mark.parametrize(
    "bikes,capacity,expected",
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (2, 10, "few bikes"),
        (8, 10, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_branches(bikes, capacity, expected):
    assert dock_status(bikes, capacity) == expected


@pytest.mark.parametrize(
    "bikes,capacity,message",
    [
        (0, 0, "invalid capacity"),
        (-1, 10, "invalid bike count"),
        (11, 10, "invalid bike count"),
    ],
)
def test_dock_status_validation_branches(bikes, capacity, message):
    with pytest.raises(ValueError, match=message):
        dock_status(bikes, capacity)


@pytest.mark.parametrize(
    "balance,active_ride,age,expected",
    [
        (500, True, 25, False),
        (500, False, 15, False),
        (99, False, 16, False),
        (100, False, 17, True),
        (49, False, 18, False),
        (50, False, 18, True),
    ],
)
def test_unlock_branches(balance, active_ride, age, expected):
    assert can_unlock(balance, active_ride, age) is expected
