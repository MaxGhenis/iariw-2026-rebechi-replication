"""Tests for shared legal and simulation constants."""

from cu_replication.constants import (
    CORP_ONLY_STATES,
    CORP_UNION_STATES,
    CPI_U,
    EXCLUDED_STATES,
    NO_INCOME_TAX_STATES,
    NO_OR_LIMITED_INCOME_TAX_STATES,
    TAXSIM_STATE_CODES,
)


def test_cpi_u_series_matches_verified_values() -> None:
    """The annual CPI-U inputs should remain unchanged."""
    expected = {
        2004: 188.900,
        2005: 195.300,
        2006: 201.600,
        2007: 207.342,
        2008: 215.303,
        2009: 214.537,
        2010: 218.056,
        2011: 224.939,
        2012: 229.594,
        2013: 232.957,
        2014: 236.736,
        2015: 237.017,
        2016: 240.007,
        2017: 245.120,
        2018: 251.107,
        2019: 255.657,
        2020: 258.811,
        2021: 270.970,
    }
    assert CPI_U == expected


def test_state_groups_are_disjoint_and_have_expected_sizes() -> None:
    """Treatment and exclusion groups should encode the paper sample."""
    groups = [set(CORP_ONLY_STATES), set(CORP_UNION_STATES), set(EXCLUDED_STATES)]
    assert [len(group) for group in groups] == [8, 13, 4]
    assert all(
        not left & right
        for i, left in enumerate(groups)
        for right in groups[i + 1 :]
    )


def test_no_income_tax_state_groups_are_explicit() -> None:
    """No-tax states should be distinct from the broader appendix exclusion."""
    assert NO_INCOME_TAX_STATES == ("AK", "FL", "NV", "TX", "WA", "WY")
    assert NO_OR_LIMITED_INCOME_TAX_STATES == (
        "AK",
        "FL",
        "NV",
        "NH",
        "TN",
        "TX",
        "WA",
        "WY",
    )


def test_taxsim_state_codes_cover_all_jurisdictions() -> None:
    """TAXSIM codes should cover every state and DC exactly once."""
    assert len(TAXSIM_STATE_CODES) == 51
    assert set(TAXSIM_STATE_CODES.values()) == set(range(1, 52))
    assert TAXSIM_STATE_CODES["AL"] == 1
    assert TAXSIM_STATE_CODES["DC"] == 9
    assert TAXSIM_STATE_CODES["WY"] == 51
