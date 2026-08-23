#!/bin/bash
# 01: Download public inputs.
# SCF "2011" in LWS = Federal Reserve SCF 2010 wave (fieldwork 2010, income year
# treated as 2010 after the Fed's own CPILAG adjustment; see NOTES.md).
# The Fed 404s scfp2011s.zip because the SCF is triennial; there is no 2011 wave.
set -e
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
mkdir -p data
curl -sL -A "$UA" -o data/scfp2010s.zip "https://www.federalreserve.gov/econres/files/scfp2010s.zip"
unzip -o -d data data/scfp2010s.zip   # -> data/rscfp2010.dta (values in 2022 dollars)
curl -sL -A "$UA" -o data/bulletin.macro.txt "https://www.federalreserve.gov/econres/files/bulletin.macro.txt"
# CPI-U annual averages verified via BLS API v2 (CUUR0000SA0, M13) on 2026-08-22.
