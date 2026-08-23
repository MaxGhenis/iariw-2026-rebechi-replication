"""Shared constants for samples, simulations, and paper comparisons."""

from __future__ import annotations

CPI_U = {
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

CORP_UNION_STATES = (
    "AK",
    "AZ",
    "MI",
    "NH",
    "NC",
    "ND",
    "OH",
    "OK",
    "PA",
    "RI",
    "TX",
    "WI",
    "WY",
)
CORP_ONLY_STATES = ("CT", "IA", "KY", "MA", "MN", "MT", "TN", "WV")
EXCLUDED_STATES = ("CO", "SD", "NE", "LA")
NO_OR_LIMITED_INCOME_TAX_STATES = (
    "AK",
    "FL",
    "NV",
    "NH",
    "TN",
    "TX",
    "WA",
    "WY",
)
REDMAP_STATES = ("MI", "OH", "PA", "TX", "NC", "WI")

ALL_JURISDICTIONS = (
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "DC",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
)

# TAXSIM's historical one-through-51 jurisdiction codes are not FIPS codes.
TAXSIM_STATE_CODES = {
    state: code
    for code, state in enumerate(
        (
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "DC",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ),
        start=1,
    )
}

OUTCOMES_TABLE4 = (
    "atr",
    "atr_top5",
    "atr_top1",
    "atr_top5nw",
    "atr_top1nw",
    "rs",
)

# Entries are (coefficient, standard error), transcribed from paper Table 4.
PAPER_TABLE4 = {
    "atr": {
        "corp_only": (0.01, 0.10),
        "corp_union": (-0.01, 0.13),
        "difference": (-0.02, 0.12),
    },
    "atr_top5": {
        "corp_only": (0.14, 0.14),
        "corp_union": (-0.33, 0.20),
        "difference": (-0.47, 0.20),
    },
    "atr_top1": {
        "corp_only": (0.30, 0.30),
        "corp_union": (-0.53, 0.24),
        "difference": (-0.83, 0.35),
    },
    "atr_top5nw": {
        "corp_only": (0.07, 0.13),
        "corp_union": (-0.25, 0.17),
        "difference": (-0.32, 0.17),
    },
    "atr_top1nw": {
        "corp_only": (0.10, 0.19),
        "corp_union": (-0.36, 0.19),
        "difference": (-0.46, 0.23),
    },
    "rs": {
        "corp_only": (0.07, 0.07),
        "corp_union": (-0.11, 0.04),
        "difference": (-0.18, 0.07),
    },
}

# The local research record preserves these Appendix B-1 references. Missing cells
# are deliberately not inferred. Entries are (coefficient, standard error or None).
PAPER_TABLE_B1 = {
    "atr_top1": {"corp_union": (-0.77, 0.30), "difference": (-1.13, None)},
    "rs": {"corp_union": (-0.12, 0.06), "difference": (-0.20, None)},
}

SCF_2022_TO_2010_DOLLAR_FACTOR = 3204 / 4376
SCF_EXPECTED_IMPLICATE_ROWS = 6_482
SCF_MONEY_COLUMNS = (
    "wageinc",
    "bussefarminc",
    "intdivinc",
    "kginc",
    "ssretinc",
    "transfothinc",
    "penacctwd",
    "income",
    "networth",
)
