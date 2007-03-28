#####################################################
#                                                   # 
#               relval_common_module                #
#                                                   #
#  Module that collects the functions to carry out  #
#  to the operations necessary for release          #
#  validation. It includes the building of the      # 
#  message logger and the IO.                       #
#                                                   #
#####################################################

__author__  = "Danilo Piparo"


import FWCore.ParameterSet.Config as cms

import relval_parameters_module as parameters

#------------------------

def add_includes(process):
    """Function to add the includes to the process.
    It returns a process enriched with the includes.
    """
    # This just simplifies the use of the logger
    mod_id = "[relval_common_module]"
    
    func_id = mod_id+"[add_includes]"
    log(func_id+" Entering... ")
    
    # Services.cfi
    services="Configuration/ReleaseValidation/data/Services.cfi"
    process.extend(cms.include(services))
    log(func_id+" Process extended with "+services)
    
    # Fake conditions 
    fake_conditions="Configuration/StandardSequences/data/FakeConditions.cff"
    process.extend(cms.include(fake_conditions))
    log(func_id+" Process extended with "+fake_conditions)
  
    # The mixingnopileup.cff file
    process.mix=cms.EDFilter("MixingModule",bunchspace=cms.int32(25))
    log(func_id+" Process extended with MixingModule ...")
    
    # The Vtxsmeared.cff file
    process.VtxSmeared=cms.EDFilter("GaussEvtVtxGenerator",
                                    MeanX=cms.double(0.),
                                    MeanY=cms.double(0.),
                                    MeanZ=cms.double(0.),
                                    SigmaX=cms.double(0.0015),
                                    SigmaY=cms.double(0.0015),
                                    SigmaZ=cms.double(5.3))  
    log(func_id+" Process extended with GaussEvtVtxGenerator ...")      
       
    # The Simulation.cff file
    # This file has been partially translated into Python so to avoid the
    # conflicts risen by the inclusion of cffs with interdipendencies.
    simulation_includes_set=("SimG4Core/Configuration/data/SimG4Core.cff",
                             "SimGeneral/TrackingAnalysis/data/trackingtruth.cfi",
                             "Configuration/StandardSequences/data/Digi.cff")
    for file in simulation_includes_set:                             
        process.extend(cms.include(file))
           
    process.psim=cms.Sequence(process.VtxSmeared+process.g4SimHits)
    process.pdigi=cms.Sequence(process.mix+\
                               process.doAllDigi+\
                               process.trackingtruth)    
    log(func_id+" Process extended with Simulation ...")
    
    # The Reconstruction.cff file
    process.extend(cms.include\
    ("Configuration/StandardSequences/data/Reconstruction.cff")) 
    
    # The file FWCore/Framework/test/cmsExceptionsFatalOption.cff:
    options=cms.untracked.PSet\
               (Rethrow=cms.untracked.vstring(
                "Unknown",
                "ProductNotFound",
                "DictionaryNotFound",
                "InsertFailure",
                "Configuration",
                "LogicError",
                "UnimplementedFeature",
                "InvalidReference",
                "NullPointerError",
                "NoProductSpecified",
                "EventTimeout",
                "EventCorruption",
                "ModuleFailure",
                "ScheduleExecutionFailure",
                "EventProcessorFailure",
                "FileInPathError",
                "FatalRootError",
                "NotFound"),
          wantSummary=cms.untracked.bool(True),
          makeTriggerResults=cms.untracked.bool(True) )
        
    log(func_id+ " Returning process...")
    return process

#-----------------------------------------

def event_input(infile_name, maxEvents=-1):
    """
    Returns the source for the process.
    """ 
    pr_source = cms.Source("PoolSource",
                           fileNames = cms.untracked.vstring\
                                     (("file:"+infile_name)),
                           maxEvents = cms.untracked.int32(-1)
                          )
    return pr_source
    
#-----------------------------------------

def event_output(process, outfile_name, step, evt_filter=None):
    """
    Function that enriches the process so to produce an output.
    """ 
    # Event content
    content=cms.include("Configuration/EventContent/data/EventContent.cff")
    process.extend(content)
    process.out_step = cms.OutputModule\
                    ("PoolOutputModule",
                     outputCommands=content.FEVTSIMEventContent.outputCommands,
                     fileName = cms.untracked.string(outfile_name),
                     datasets = cms.untracked.PSet(dataset1 =cms.untracked.PSet\
                                        (dataTier =cms.untracked.string(step)))
                    )
    
    process.outpath = cms.EndPath(process.out_step)
    
    return process 
    
#-----------------------------------------

def build_message_logger():
    """
    Function that returns the message logger service
    """
    msg_logger=cms.include("FWCore/MessageService/data/MessageLogger.cfi")
    msg_logger.MessageLogger.cout.threshold = "ERROR"
    msg_logger.MessageLogger.cerr.default.limit = 10
    
    return msg_logger

#--------------------------------------------

def build_profiler_service(process,evts_cuts):
    """
    A profiler service by Vincenzo Innocente.
    """
    firstevent=int(evts_cuts.split("_")[0])
    lastevent= int(evts_cuts.split("_")[1])

    prof_service=cms.Service("ProfilerService",
                             firstEvent=cms.untracked.int32(firstevent),
                             lastEvent=cms.untracked.int32(lastevent),
                             paths=cms.untracked.vstring("ALL")                        
                            )
    return prof_service
    
#--------------------------------------------------- 

def build_production_info():
    """
    Add useful info for the production.
    """
    prod_info=cms.untracked.PSet\
              (
               version=cms.untracked.string("$Revision: 1.4 $"),
               name=cms.untracked.string("$Name: V00-01-00 $"),
               annotation=cms.untracked.string\
                                ("PyRelVal")
              )
    return prod_info 
                                   
#--------------------------------------------

def log (message):
    """
    An oversimplified logger. This is designed for debugging the PyReleaseValidation
    """
    if parameters.dbg_flag:
        print message
