################################################
#                                              # 
#         relval_digireco_module:              #
#  This module includes the functions used to  #
#  define the digitisation and reconstruction  #
#  processes.                                  #
#                                              #
################################################

__author__  = "Danilo Piparo"


import FWCore.ParameterSet.Config as cms

import relval_common_module as common

#-----------------------------------------
# This simplifies the use of the logger
mod_id = "[relval_digireco_module]"
#-----------------------------------------

def digitise(process, step, infile_name):
    """Function that produces the digitisation starting 
    from the sim rootfile. It returns the enhanced process. 
    """
    func_id=mod_id+"[digitise]"
    common.log(func_id+"Entering ...") 
   
    # Disable IO when all the steps are to be performed at once.
    if not step == "ALL":    
        process = common.event_input(process, infile_name)
    
    #process.digitisation_step = cms.Path(process.pdigi)
        
    common.log(func_id+" Returning the process..")
    
    return process

#----------------------------------------- 
  
def reconstruct (process, step, infile_name):
    """Function that produces the reconstruction starting 
    from the sim rootfile. It returns the enhanced process. 
    """
    func_id=mod_id+"[reconstruct]"
    common.log(func_id+" Entering ...")

    # Disable IO when all the steps are to be performed at once.
    if not step == "ALL":   
        process = common.event_input(process, infile_name)
        
    #process.reconstruction_step = cms.Path (process.reconstruction)
            
    common.log(func_id+" Returning the process..")
    
    return process
   
#-------------------------------------------

def _process_IO (process, infile_name, step):
    
    func_id=mod_id+"[_process_IO]"
    common.log(func_id+"Entering ...")

    # Event Input
    process = common.event_input(process, infile_name)
    # Event output
    #process = common.event_output(process, outfile_name, step) 
    return process
    
#-------------------------------------------