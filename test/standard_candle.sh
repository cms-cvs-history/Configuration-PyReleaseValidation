#! /bin/sh

echo A standard candle benchmark: QCD with 20GeV < Pt < 30GeV.
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n10 -e20_30 -sALL
