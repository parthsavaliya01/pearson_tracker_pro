import pytest

from src.counter import PeopleCounter


def test_counter_tracks_entry_and_exit_without_negative_occupancy():
    counter = PeopleCounter()

    # Simulate a person moving from left to right across the line.
    counter.update([[100, 100, 140, 180]], [101])
    counter.update([[320, 100, 360, 180]], [101])
    counter.update([[380, 100, 420, 180]], [101])

    total, current, entered, exited = counter.update([[420, 100, 460, 180]], [101])

    assert total == 1
    assert current == 1
    assert entered == 1
    assert exited == 0

    # Simulate the same person leaving back across the line.
    counter.update([[300, 100, 340, 180]], [101])
    counter.update([[250, 100, 290, 180]], [101])
    counter.update([[200, 100, 240, 180]], [101])

    total, current, entered, exited = counter.update([[150, 100, 190, 180]], [101])

    assert total == 1
    assert current == 0
    assert entered == 1
    assert exited == 1


def test_counter_does_not_double_count_same_crossing():
    counter = PeopleCounter()

    counter.update([[100, 100, 140, 180]], [201])
    counter.update([[320, 100, 360, 180]], [201])
    counter.update([[380, 100, 420, 180]], [201])
    total, current, entered, exited = counter.update([[420, 100, 460, 180]], [201])

    assert entered == 1
    assert exited == 0

    total, current, entered, exited = counter.update([[430, 100, 470, 180]], [201])
    assert entered == 1
    assert exited == 0
