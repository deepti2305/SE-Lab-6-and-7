import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---- fuel_bill: validation branches ----
@pytest.mark.parametrize("grade", ["kerosene", "", "REGULAR"])
def test_unknown_grade_raises(grade):
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill(grade, 10, "silver")


def test_negative_litres_raises():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_zero_litres_is_free():
    assert fuel_bill("regular", 0, "silver") == 0


# ---- gold bonus: true/false for each part of the condition ----
def test_gold_non_diesel_gets_bonus():
    assert fuel_bill("premium", 20, "gold") == 0       # covered 15+5
    assert fuel_bill("premium", 21, "gold") == 1 * 105


def test_gold_diesel_no_bonus():
    assert fuel_bill("diesel", 21, "gold") == 1 * 90


def test_non_gold_no_bonus():
    assert fuel_bill("premium", 16, "silver") == 1 * 105


# ---- extra <= 0 boundary ----
def test_extra_exactly_zero():
    assert fuel_bill("regular", 10, "silver") == 0


def test_extra_just_above_zero():
    assert fuel_bill("regular", 11, "silver") == 105


# ---- rate selection ----
def test_diesel_rate():
    assert fuel_bill("diesel", 25, "silver") == 5 * 90


def test_non_diesel_rate():
    assert fuel_bill("premium", 20, "silver") == 5 * 105


# ---- bulk discount boundary: extra == 30 vs 31 ----
def test_extra_exactly_30_no_discount():
    assert fuel_bill("regular", 40, "silver") == 30 * 105


def test_extra_31_discount_non_gold():
    assert fuel_bill("regular", 41, "silver") == 31 * 99


def test_extra_31_discount_gold():
    assert fuel_bill("regular", 46, "gold") == 31 * 95       # covered 15


def test_extra_30_gold_no_discount():
    assert fuel_bill("regular", 45, "gold") == 30 * 105


def test_bulk_diesel_gold():
    assert fuel_bill("diesel", 51, "gold") == 31 * 80


def test_bulk_diesel_non_gold():
    assert fuel_bill("diesel", 51, "silver") == 31 * 84


# ---- pump_allowed ----
def test_fleet_boundary_200():
    assert pump_allowed(200, 9, True) is True


def test_fleet_over_200():
    assert pump_allowed(201, 1, True) is False


def test_non_fleet_over_60():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_exactly_60_one_container():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_two_containers():
    assert pump_allowed(30, 2, False) is False


def test_non_fleet_zero_containers():
    assert pump_allowed(30, 0, False) is True


# ---- session_status: cutoffs 30 / 60 / 60 / 90 ----
@pytest.mark.parametrize("card,night,cutoff", [
    (False, False, 30), (True, False, 60), (False, True, 60), (True, True, 90)])
def test_session_boundaries(card, night, cutoff):
    assert session_status(cutoff, card, night) == "active"
    assert session_status(cutoff - 1, card, night) == "warning"
    assert session_status(cutoff - 15, card, night) == "warning"
    assert session_status(cutoff - 16, card, night) == "timed_out"
    assert session_status(0, card, night) == "timed_out"
