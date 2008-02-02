###################################################
#                                                 #
#                 relval_main                     #
#                                                 #              
#  Release validation main file. It initialises   #
#  the process and uses the informations kept in  #
#  relval_parameters_module to build the object.  #
#                                                 #
###################################################

__author__="Danilo Piparo"

# Let Python find the parameters module created locally in the current directory.
# As long as the Python code cannot have any command line arguments since this could lead
# to conflicts with cmsRun this is a way to input 
import sys
import pickle
import os

# Modules to include

import FWCore.ParameterSet.Config as cms

#import relval_parameters_module as parameters
#Try to eliminate the problem of the _commonsequence without the import
execfile("relval_parameters_module.py")

import relval_common_module as common
import relval_steps_module as steps 

sys.path.append(".") # necessary to find the relval_parameters_module created by CMSdriver
   
#---------------------------------------------------

# Here the process is built according to the settings in
# the relval_parameters_module. All the objects built have in 
# common the features described in the relval_common_module.

print "\nPython RelVal"
 
process = cms.Process (process_name)
         
process.schedule=cms.Schedule()

# Enrich the process with the features described in the relval_includes_module.
process=common.add_includes(process,PU_flag)

# Add the fpe service if needed:
if fpe_service_flag:
    process.add_(common.build_fpe_service()) 

# Add the Profiler Service if needed:
if profiler_service_cuts!="":
    process.add_(common.build_profiler_service(profiler_service_cuts))

# Set the number of events with a top level PSet
process.maxEvents=cms.untracked.PSet(input=cms.untracked.int32(evtnumber))

# Add the ReleaseValidation PSet
totnumevts,evtsperjob=releasevalidation
dsetname="RelVal"+ext_process_name
if dump_pickle!='':
    dsetname=dump_pickle
process.ReleaseValidation=cms.untracked.PSet(totalNumberOfEvents=cms.untracked.int32(totnumevts),
                                             eventsPerJob=cms.untracked.int32(evtsperjob),
                                             primaryDatasetName=cms.untracked.string(dsetname.replace('.pkl','')))

"""
Here we choose to make the process work only for one of the four steps 
(GEN,SIM DIGI RECO) or for the whole chain (ALL)
"""

# parse the string containing the steps and make a list out of it
if step=='ALL':
    step='GEN,SIM,DIGI,L1,DIGI2RAW,RECO'
step_list=step.split(',') # we split when we find a ','

# a dict whose keys are the steps and the values are functions that modify the process
# in order to add the actual step..
step_dict={'GEN':steps.gen,
           'SIM':steps.sim,
           'DIGI':steps.digi,
           'RECO':steps.reco,
           'L1':steps.l1_trigger,
           'DIGI2RAW':steps.digi2raw,
           'ANA':steps.ana}

# we add a source even if gen is not present.
if not 'GEN' in step_list:
    process.source = common.event_input(infile_name) 
else:
    process=steps.gen(process,step,evt_type,energy,evtnumber)           
for step in step_list:
    if step in ('ANA','GEN'):
        continue
    process=step_dict[step](process)                      

# Analysis
if 'ANA' in step:
    steps.ana(process)
    
# Add the output on a root file if requested
if output_flag:
    process = common.event_output\
        (process, outfile_name, step)
    if not user_schedule:
        process.schedule.append(process.outpath)  
                                                                        

# Add metadata for production                                    
process.configurationMetadata=common.build_production_info(evt_type, energy, evtnumber) 

# Add a last customisation of the process as specified in the file.
if customisation_file!='':
    file=__import__(customisation_file[:-3])
    process=file.customise(process)

# print to screen the config file in the old language
if dump_cfg_flag:
    #print process.dumpConfig()
    print process.dumpPython()
    sys.exit()
    

# print to screen the config file in the python language
if dump_python!='':
    pycfg=open(dump_python,'w') 
    pycfg.write('import FWCore.ParameterSet.Config as cms \n')
    pycfg.write(process.dumpPython())
    pycfg.close()


# dump a pickle object of the process on disk:
if dump_pickle!='':
   print "Dumping process on disk as a pickle object..."
   pickle_file=file(dump_pickle,"w")
   pickle.dump(process,pickle_file)
   pickle_file.close()
   sys.exit() # no need to launch the FW
       
# A sober separator between the python program and CMSSW    
print "And now The Framework -----------------------------"
