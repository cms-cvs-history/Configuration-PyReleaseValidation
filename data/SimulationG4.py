#G.Benelli Dec 21 2007
#This fragment is used for the simulation (SIM) step
#It includes a MessageLogger tweak to dump G4msg.log
#in addition to the the SimpleMemoryCheck and Timing
#services output for the log of the simulation
#performance candles.
#It is meant to be used with the cmsDriver.py option
#--customise in the following fashion:
#E.g.
#./cmsDriver.py HZZLLLL -e 190 -n 50 --step=SIM --customise=SimulationG4.py >& HZZLLLL_190_GEN.log&
#or
#./cmsDriver.py MINBIAS -n 50 --step=SIM --customise=SimulationG4.py >& MINBIAS_GEN.log&


import FWCore.ParameterSet.Config as cms
def customise(process):
    #Adding SimpleMemoryCheck service:
    process.SimpleMemoryCheck=cms.Service("SimpleMemoryCheck",
                                          ignoreTotal=cms.untracked.int32(1),
                                          oncePerEventMode=cms.untracked.bool(True))
    #Adding Timing service:
    process.Timing=cms.Service("Timing")
    
    #Tweak Message logger to dump G4cout and G4cerr messages in G4msg.log
    #print process.MessageLogger.__dict__
    process.MessageLogger.destinations=cms.untracked.vstring('warnings'
                                                             , 'errors'
                                                             , 'infos'
                                                             , 'debugs'
                                                             , 'cout'
                                                             , 'cerr'
                                                             , 'G4msg'
                                                             )
    process.MessageLogger.categories=cms.untracked.vstring('FwkJob'
                                                           ,'FwkReport'
                                                           ,'FwkSummary'
                                                           ,'Root_NoDictionary'
                                                           ,'G4cout'
                                                           ,'G4cerr'
                                                           )
    process.MessageLogger.cerr = cms.untracked.PSet(
        noTimeStamps = cms.untracked.bool(True)
        )
    process.MessageLogger.G4msg =  cms.untracked.PSet(
        noTimeStamps = cms.untracked.bool(True)
        ,threshold = cms.untracked.string('INFO')
        ,INFO = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,G4cout = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,G4cerr = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        )
    return(process)
