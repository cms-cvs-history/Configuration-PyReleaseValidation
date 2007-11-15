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
import cPickle
import os

sys.path.append(".") # necessary to find the relval_parameters_module created by CMSdriver

# Modules to include

import FWCore.ParameterSet.Config as cms

#import relval_parameters_module as parameters
#Try to eliminate the problem of the _commonsequence without the import
execfile("relval_parameters_module.py")

import relval_common_module as common
#import relval_simulation_module
execfile(os.environ["CMSSW_BASE"]+\
    "/src/Configuration/PyReleaseValidation/data/relval_generation_module.py")

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
process.ReleaseValidation=cms.untracked.PSet(totalNumberOfEvents=cms.untracked.int32(5000),
                                             eventsPerJob=cms.untracked.int32(250),
                                             primaryDatasetName=cms.untracked.string("RelVal"+ext_process_name))

"""
Here we choose to make the process work only for one of the four steps 
(GEN,SIM DIGI RECO) or for the whole chain (ALL)
"""



# The Generation:
if step in ("ALL","GEN","GENSIM"):
    # Builds the source for the process
    process.source=generate(step,evt_type,energy,evtnumber)
                                                  
# The Simulation, Digitisation and Reconstruction:
else: # The input is a file
    process.source = common.event_input(infile_name) 

if step in ("ALL","SIM","GENSIM"):
    # Enrich the schedule with simulation
    process.simulation_step = cms.Path(process.psim)
    process.schedule.append(process.simulation_step)    
     
if step in ("ALL","DIGI","DIGIRECO","DIGIPURECO"):
    process.digitisation_step=cms.Path(process.pdigi)
    process.schedule.append(process.digitisation_step)
       
if step in ("ALL","RECO","DIGIRECO","DIGIPURECO"):
    if newstep3list!=[]: #add user defined elements for reco
        for element in newstep3list:
            exec("process."+element+"_step=cms.Path(process.sequences[element])")
            exec("process.schedule.append(process."+element+"_step)")
    else:
        process.reconstruction_step=cms.Path(process.reconstruction_plusRS)
        process.schedule.append(process.reconstruction_step)     

# L1 trigger      
if step in ("ALL","RECO","DIGIRECO","DIGIPURECO"):
    common.log("Adding L1 emulation... ")
    process.L1_Emulation = cms.Path(process.L1Emulator)
    process.schedule.append(process.L1_Emulation)

# Analysis
if analysis_flag:
    common.log("Adding Analysis... ")
    process.analysis_step=cms.Path(process.analysis)
    process.schedule.append(process.analysis_step)
                                             
# Add the output on a root file if requested
if output_flag:
    process = common.event_output\
        (process, outfile_name, step)
    process.schedule.append(process.outpath)  
                                                                        

# Add metadata for production                                    
process.configurationMetadata=common.build_production_info(evt_type, energy, evtnumber) 


# print to screen the config file in the old language
if dump_cfg_flag:
    print process.dumpConfig()
    

# dump a pickle object of the process on disk:
if dump_pickle_flag:
   print "Dumping process on disk as a pickle object..."
   pickle_file=file(ext_process_name+".pkl","w")
   cPickle.dump(process,pickle_file)
   pickle_file.close()
   sys.exit() # no need to launch the FW
       
# A sober separator between the python program and CMSSW    
print "And now The Framework -----------------------------"
