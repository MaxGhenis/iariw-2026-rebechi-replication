"""02: Build the fixed household sample for TAXSIM from the SCF 2010 summary extract.

Dollar conversion (verified from data/bulletin.macro.txt, the Fed's own generator):
  published rscfp2010.dta values = nominal * CPILAG * CPIADJ where, for 2010,
  CPILAG = 3198/3147 (income vars only: income-year-2009 -> 2010 dollars, CPI-U-RS)
  CPIADJ = 4376/3204 (all dollar vars: Sept-2010 -> Sept-2022 CPI-U-RS)
  We multiply ALL dollar vars by 3204/4376, recovering incomes in 2010 dollars
  (the Fed's own "2010 dollars" convention, which already lags 2009 income to 2010)
  and net worth in 2010 dollars. This matches the paper's treatment of the LWS/SCF
  data as 2010 incomes (paper footnote 8).

TAXSIM input mapping (summary-extract limits; see REPORT.md caveats):
  mstat   : married==1 -> "married, jointly" (includes cohabiting partners), else "single"
            (TAXSIM-35 treats single filers with dependents as heads of household)
  page    : age of head; sage = age of head if married (spouse age not in extract)
  depx    : kids (dependent ages set to 10 for first three -> all CTC/EITC-qualifying)
  pwages/swages : wageinc split 60/40 if married, else all to pwages
  psemp   : bussefarminc (= business/farm/self-emp INCLUDING rent+royalties X5714)
  dividends/intrec : intdivinc split 50/50
  ltcg    : kginc (can be negative)
  pensions: ssretinc + penacctwd (Social Security cannot be separated from pensions
            in the extract -> ALL treated as taxable pension income; overstates state
            tax for SS recipients in states that exempt SS but tax pensions)
  transfers: max(transfothinc,0); negative part -> otherprop
  itemized deductions, property tax, mortgage, childcare, stcg, ui: 0 (not available)
Implicate 1 only (y1 % 10 == 1), n = 6,482; weight = wgt.
"""
import pyreadstat
import pandas as pd
import numpy as np

CPIADJ = 4376 / 3204  # published = 2010$ * CPIADJ

df, _ = pyreadstat.read_dta("data/rscfp2010.dta")
d = df[df.y1 % 10 == 1].copy().reset_index(drop=True)
assert len(d) == 6482, len(d)

money = ["wageinc", "bussefarminc", "intdivinc", "kginc", "ssretinc",
         "transfothinc", "penacctwd", "income", "networth"]
for c in money:
    d[c] = d[c] / CPIADJ  # -> 2010 dollars

out = pd.DataFrame({
    "hhid": np.arange(1, len(d) + 1),
    "wgt": d.wgt,
    "mstat": np.where(d.married == 1, "married, jointly", "single"),
    "page": d.age.astype(int),
    "sage": np.where(d.married == 1, d.age, 0).astype(int),
    "depx": d.kids.astype(int),
    "age1": np.where(d.kids >= 1, 10, 0),
    "age2": np.where(d.kids >= 2, 10, 0),
    "age3": np.where(d.kids >= 3, 10, 0),
    "pwages": np.where(d.married == 1, 0.6 * d.wageinc, d.wageinc),
    "swages": np.where(d.married == 1, 0.4 * d.wageinc, 0.0),
    "psemp": d.bussefarminc,
    "dividends": 0.5 * d.intdivinc,
    "intrec": 0.5 * d.intdivinc,
    "ltcg": d.kginc,
    "pensions": d.ssretinc + d.penacctwd,
    "transfers": d.transfothinc.clip(lower=0),
    "otherprop": d.transfothinc.clip(upper=0),
    "scf_income": d.income,       # 2010$, Fed definition (for reference only)
    "networth": d.networth,       # 2010$
})
out.to_csv("data/base_households.csv", index=False)
print("wrote data/base_households.csv", out.shape)
print(out[["pwages", "psemp", "dividends", "ltcg", "pensions", "transfers",
           "otherprop", "scf_income", "networth"]].describe().round(1).to_string())
