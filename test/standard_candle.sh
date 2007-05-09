#! /bin/sh

echo A standard candle benchmark: QCD with 20GeV < Pt < 30GeV.

echo Getting ready Sim and Digi steps and run the reco without output.
$CMSSW_BASE/src/Configuration/PyReleaseValidation/test/relvalreport.py 12 3 RECO 15 3_13 0