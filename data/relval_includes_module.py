##############################################
#                                            #
#         relval_includes_module             #
#                                            #
#  A module where the includes necessary to  #
#  the release validation are stored.        #
#                                            #
##############################################

__author__  = "Danilo Piparo"

import FWCore.ParameterSet.Config as cms

import relval_common_module as common

#---------------------------------------------------
# This just simplifies the use of the logger
mod_id = "[relval_includes_module]"
#--------------------------------------------------- 

def add_includes(process, msg_logger_flag=True):
    """Function to add the includes to the process.
    The msg_logger_flag allow to decide whether to put the message logger or not.
    It returns a process enriched with the includes.
    """
    func_id = mod_id+"[add_includes]"
    common.log( func_id+" Entering... ")
   
    fake_conditions=\
            "Configuration/StandardSequences/data/FakeConditions.cff"
    process.extend( cms.include(fake_conditions) )
    common.log(func_id+" Process extended with "+fake_conditions)
  
    # The mixingnopileup.cff file
    process.mix=cms.EDFilter("MixingModule",bunchspace=cms.int32(25))
    common.log(func_id+" Process extended with MixingModule ...")
    
    # The Vtxsmeared.cff file
    process.VtxSmeared=cms.EDFilter("GaussEvtVtxGenerator",
                                    MeanX=cms.double(0.),
                                    MeanY=cms.double(0.),
                                    MeanZ=cms.double(0.),
                                    SigmaX=cms.double(0.0015),
                                    SigmaY=cms.double(0.0015),
                                    SigmaZ=cms.double(5.3))  
    common.log(func_id+" Process extended with GaussEvtVtxGenerator ...")      
       
    # The Simulation.cff file
    # This file has been partially translated into Python so to avoid the
    # conflicts risen by the inclusion of cffs with interdipendencies.
    process.extend(cms.include\
    ("SimG4Core/Configuration/data/SimG4Core.cff"))
    process.extend(cms.include\
    ("SimGeneral/TrackingAnalysis/data/trackingtruth.cfi"))
    process.extend(cms.include\
    ("Configuration/StandardSequences/data/Digi.cff"))     
    process.psim=cms.Sequence(process.VtxSmeared+process.g4SimHits)
    process.pdigi=cms.Sequence(process.mix+\
                               process.doAllDigi+\
                               process.trackingtruth)    
    common.log(func_id+" Process extended with Simulation ...")
    
    # The Reconstruction.cff file
    process.extend(cms.include\
    ("Configuration/StandardSequences/data/Reconstruction.cff")) 
    
    # Options
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
    
    # Message logger
    if msg_logger_flag:
        process = common.message_logger(process)
    
    common.log(func_id+ " Returning process...")
    return process
 
#--------------------------------------------------- 

def add_production_info(process):
    """
    Add useful info for the production
    """
    process.configurationMetadata=cms.untracked.PSet\
              (
               version=cms.untracked.string("$Revision: 1.2 $"),
               name=cms.untracked.string("$Name:  $"),
               annotation=cms.untracked.string\
                                ("PyRelVal")
              )
    return process
   
#---------------------------------------------------