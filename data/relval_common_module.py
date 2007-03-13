###############################################
#                                             # 
#        relval_common_module                 #
#                                             #
#  Module that collects the functions common  #
#  to the operations necessary for release    #
#  validation                                 #
#                                             #
###############################################

__author__  = "Danilo Piparo"


import FWCore.ParameterSet.Config as cms

import relval_parameters_module as parameters

#-----------------------------------------

def event_input(process, infile_name, maxEvents=-1): 
    process.source = cms.Source("PoolSource",
                                 fileNames = cms.untracked.vstring\
                                              (("file:"+infile_name)),
                                 maxEvents = cms.untracked.int32(-1)
                               )
    return process
    
#-----------------------------------------

def event_output(process, outfile_name, step, evt_filter=None):
      
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

def message_logger(process):
    """
    Function that adds to the process the message logger service
    """
    
    # Message logger
    process.extend(cms.include("FWCore/MessageService/data/MessageLogger.cfi"))
    process.MessageLogger.cout.threshold = "ERROR"
    process.MessageLogger.cerr.default.limit = 10
    
    return process
   
#--------------------------------------------

def log (message):
 """
 An oversimplified logger for debugging purposes.
 """
 if parameters.dbg_flag:
  print message

#--------------------------------------------

def print_dict(dict):
 '''
 A simple function to show the options of the program.
 ''' 
 dictkeys = dict.keys()
 dictkeys.sort()
 print "\n"
 print "Parameters |--------------------\n"
 for key in dictkeys:
  print key +": "+ str( dict[key]) 
 print "\n----------------------\n"
