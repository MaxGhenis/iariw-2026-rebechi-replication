#!/usr/bin/env Rscript
# 03: Run TAXSIM-35 (local WebAssembly via usincometaxes) for all 51 jurisdictions
# x requested years. Usage: Rscript scripts/03_run_taxsim.R <year_from> <year_to>
# Writes data/taxsim_out_<year>.csv per year (checkpointed; skips existing).
#
# Deflation (paper footnote 8): 2010-dollar incomes scaled to year t by
# CPI-U(t)/CPI-U(2010). CPI-U annual averages verified against BLS API 2026-08-22.
# Honor ordinary R library configuration. Retain the original local-library
# location as a compatibility fallback when it exists.
local_lib <- path.expand("~/Rlibs")
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
suppressMessages(library(usincometaxes))

cpi <- c(`2004`=188.9, `2005`=195.3, `2006`=201.6, `2007`=207.342, `2008`=215.303,
         `2009`=214.537, `2010`=218.056, `2011`=224.939, `2012`=229.594, `2013`=232.957,
         `2014`=236.736, `2015`=237.017, `2016`=240.007, `2017`=245.120, `2018`=251.107,
         `2019`=255.657, `2020`=258.811, `2021`=270.970)

states <- c(state.abb, "DC")  # 51 jurisdictions
base <- read.csv("data/base_households.csv", stringsAsFactors = FALSE)
money_cols <- c("pwages","swages","psemp","dividends","intrec","ltcg",
                "pensions","transfers","otherprop")
keep_out <- c("taxsimid","fiitax","siitax","v10_federal_agi","v32_state_agi")

args <- commandArgs(trailingOnly = TRUE)
yfrom <- as.integer(args[1]); yto <- as.integer(args[2])

for (yr in yfrom:yto) {
  f <- sprintf("data/taxsim_out_%d.csv", yr)
  if (file.exists(f)) { cat(yr, "exists, skip\n"); next }
  defl <- cpi[as.character(yr)] / cpi["2010"]
  inp0 <- data.frame(
    taxsimid = base$hhid, year = yr, mstat = base$mstat,
    page = base$page, sage = base$sage, depx = base$depx,
    age1 = base$age1, age2 = base$age2, age3 = base$age3,
    base[money_cols] * defl,
    stringsAsFactors = FALSE)
  res <- vector("list", length(states))
  t0 <- Sys.time()
  for (i in seq_along(states)) {
    st <- states[i]
    inp <- inp0; inp$state <- st
    out <- suppressMessages(taxsim_calculate_taxes(inp, return_all_information = TRUE))
    out <- as.data.frame(out)[, keep_out]
    out$state <- st
    res[[i]] <- out
  }
  allout <- do.call(rbind, res)
  allout$year <- yr
  write.csv(allout, f, row.names = FALSE)
  cat(sprintf("year %d done in %.1f min, %d rows\n", yr,
              as.numeric(difftime(Sys.time(), t0, units = "mins")), nrow(allout)))
}
