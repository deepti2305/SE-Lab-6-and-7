import builtins
import contextlib
import io
import math

from hypothesis import given, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill, main

anything = st.text() | st.none() | st.integers() | st.floats() | st.binary() | st.lists(st.integers())


# ---------------- parse_purchase ----------------
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    parse_purchase(s)


@given(anything)
def test_parse_purchase_any_type_no_crash(s):
    parse_purchase(s)


@given(st.text() | st.none())
def test_parse_purchase_return_shape(s):
    grade, litres = parse_purchase(s)
    assert isinstance(grade, str)
    assert isinstance(litres, float)
    assert math.isfinite(litres) and litres >= 0


@given(st.text(alphabet=st.characters(whitelist_categories=("L",), max_codepoint=127), min_size=1),
       st.floats(min_value=0, max_value=1e6))
def test_parse_purchase_valid_roundtrip(grade, litres):
    g, l = parse_purchase(f"{grade}:{litres}")
    assert g == grade.strip().title()
    assert l == litres


# ---------------- volume_average ----------------
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    volume_average(s)


@given(anything)
def test_volume_average_any_type_no_crash(s):
    volume_average(s)


@given(st.text() | st.none())
def test_volume_average_return_type(s):
    r = volume_average(s)
    assert isinstance(r, (int, float)) and math.isfinite(r) and r >= 0


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_volume_average_within_bounds(vals):
    r = volume_average(",".join(map(str, vals)))
    assert min(vals) <= r <= max(vals)
    assert r == sum(vals) // len(vals)


@given(st.lists(st.text()))
def test_volume_average_joined_text_no_crash(parts):
    volume_average(",".join(parts))


# ---------------- payable_bill ----------------
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    payable_bill(s)


@given(anything)
def test_payable_bill_any_type_no_crash(s):
    payable_bill(s)


@given(st.text() | st.none())
def test_payable_bill_non_negative_finite(s):
    r = payable_bill(s)
    assert isinstance(r, (int, float)) and math.isfinite(r) and r >= 0


@given(st.floats(min_value=0, max_value=1e9), st.floats(min_value=0, max_value=1e9))
def test_payable_bill_valid_formula(bill, discount):
    r = payable_bill(f"{bill}|{discount}")
    assert math.isclose(r, max(bill * 1.18 - discount, 0), rel_tol=1e-9, abs_tol=1e-9)


@given(st.text(), st.text())
def test_payable_bill_two_text_fields_no_crash(a, b):
    payable_bill(f"{a}|{b}")


# ---------------- main ----------------
@given(st.text(alphabet=st.characters(blacklist_characters="\n\r"), max_size=30),
       st.text(alphabet=st.characters(blacklist_characters="\n\r"), max_size=30),
       st.text(alphabet=st.characters(blacklist_characters="\n\r"), max_size=30))
def test_main_no_crash(a, b, c):
    inputs = iter([a, b, c])
    orig = builtins.input
    builtins.input = lambda prompt="": next(inputs)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            main()
    finally:
        builtins.input = orig
