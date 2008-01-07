import FWCore.ParameterSet.Config as cms
import relval_common_module as common

import os
import sys 

# This just simplifies the use of the common.logger
mod_id="["+os.path.basename(sys._getframe().f_code.co_filename)[:-3]+"]"

# At top level and not in a function. To be fixed
# The priority with wich the generators module is seeked for..
generator_module_name="relval_generation_module.py"
generator_releasebase_location=os.environ["CMSSW_RELEASE_BASE"]+"/src/Configuration/Generator/test/"+generator_module_name
generator_location=os.environ["CMSSW_BASE"]+"/src/Configuration/Generator/test/"+generator_module_name
pyrelval_location=os.environ["CMSSW_BASE"]+"/src/Configuration/PyReleaseValidation/data/"+generator_module_name

locations=(generator_releasebase_location,
        generator_location,
        pyrelval_location)
        
mod_location=""
for location in locations:
    if os.path.exists(location):
        mod_location=location

print 'mod_location %s' % mod_location
execfile(mod_location)
print generate

#--------------------------------------------
# Here the functions to add to the process the various steps are defined:
# Build a dict whose keys are the step names and whose values are the functions that 
# add to the process schedule the steps.
def gen(process,step,evt_type,energy,evtnumber):
    '''
    Builds the source for the process
    '''
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    

    process.source=generate(step,evt_type,energy,evtnumber)
    
    common.log ('%s adding step ...'%func_id)
    return process
    
def sim(process):
    '''
    Enrich the schedule with simulation
    '''
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.simulation_step = cms.Path(process.psim)
    process.schedule.append(process.simulation_step)  
    
    common.log ('%s adding step ...'%func_id)
    return process
   
def digi(process):
    '''
    Enrich the schedule with digitisation
    '''
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.digitisation_step=cms.Path(process.pdigi)
    process.schedule.append(process.digitisation_step)
    
    common.log ('%s adding step ...'%func_id)
    
    return process            
       
def reco(process):
    '''
    Enrich the schedule with reconstruction
    '''
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.reconstruction_step=cms.Path(process.reconstruction_plusRS_plus_GSF)
    process.schedule.append(process.reconstruction_step)     

    common.log ('%s adding step ...'%func_id)
    
    return process            

def l1_trigger(process):
    '''
    Enrich the schedule with L1 trigger
    '''     
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.L1_Emulation = cms.Path(process.L1Emulator)
    process.schedule.append(process.L1_Emulation)

    common.log ('%s adding step ...'%func_id)
    
    return process            
    
def ana(process):
    '''
    Enrich the schedule with analysis
    '''     
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.analysis_step=cms.Path(process.analysis)
    process.schedule.append(process.analysis_step)

    common.log ('%s adding step ...'%func_id)
    
    return process            

def digi2raw(process):
    '''
    Enrich the schedule with raw2digistep
    '''     
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    
    process.digi2raw_step=cms.Path(process.DigiToRaw)
    process.schedule.append(process.digi2raw_step)
    
    common.log ('%s adding step ...'%func_id)
    
    return process
