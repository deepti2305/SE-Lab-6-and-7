import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


def test_unknown_grade():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 10, "silver")


def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -1, "silver")


def test_regular_extra_normal_rate():
    assert fuel_bill("regular", 20, "silver") == 10 * 105


def test_diesel_extra_normal_rate():
    assert fuel_bill("diesel", 30, "silver") == 10 * 90


def test_gold_regular_gets_bonus_litres():
    assert fuel_bill("regular", 15, "gold") == 0


def test_bulk_discount_regular():
    assert fuel_bill("regular", 50, "silver") == 40 * 99


def test_bulk_discount_gold_regular():
    assert fuel_bill("regular", 50, "gold") == 35 * 95


def test_bulk_discount_diesel():
    assert fuel_bill("diesel", 60, "gold") == 40 * 80


def test_pump_fleet():
    assert pump_allowed(150, 5, True) is True


def test_pump_too_many_litres():
    assert pump_allowed(61, 1, False) is False


def test_pump_too_many_containers():
    assert pump_allowed(30, 2, False) is False


def test_session_active_card_day():
    assert session_status(60, True, False) == "active"


def test_session_warning_cash_night():
    assert session_status(50, False, True) == "warning"


def test_session_timed_out():
    assert session_status(0, False, False) == "timed_out"
