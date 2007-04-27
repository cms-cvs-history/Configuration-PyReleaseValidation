#! /bin/sh

#Dummy script to run all integration tests

NEVTS=10
STEP=ALL

$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU+ -n$NEVTS -e1 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU- -n$NEVTS -e1 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e380_470 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU+ -n$NEVTS -e10 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py HZZMUMUMUMU -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py E- -n$NEVTS -e35 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py TAU -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU- -n$NEVTS -e100 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e300_380 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py UDS_JETS -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU- -n$NEVTS -e10 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e120_170 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py 10MU- -n$NEVTS -e1_10 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py ZPJJ -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e170_230 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py B_JETS -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py HZZEEEE -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py MU+ -n$NEVTS -e100 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e800_1000 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py GAMMA -n$NEVTS -e35 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py GAMMA -n$NEVTS -e10 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py TTBAR -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py C_JETS -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e50_80 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e80_120 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e15_20 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py ZEE -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e230_300 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e470_600 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e600_800 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e20_30 -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py BSJPSIPHI -n$NEVTS -s$STEP
$CMSSW_BASE/src/Configuration/PyReleaseValidation/data/cmsDriver.py QCD -n$NEVTS -e30_50 -s$STEP
