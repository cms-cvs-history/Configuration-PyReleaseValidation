###################################################
#                                                 #
#                 relval_main                     #
#                                                 #              
#  Release validation main file. It initialises   #
#  the process and uses the informations kept in  #
#  relval_parameters_module to build the object.  #
#                                                 #
###################################################

__author__  = "Danilo Piparo"

# Let Python find the parameters module created locally in the current directory.
# As long as the Python code cannot have any command line arguments since this could lead
# to conflicts with cmsRun this is a way to input parameters.
import sys
sys.path.append(".")

# Modules to include

import FWCore.ParameterSet.Config as cms

import relval_parameters_module as parameters
import relval_common_module as common
import relval_includes_module as includes
import relval_digireco_module
import relval_simulation_module

#---------------------------------------------------

# Here the process is built according to the settings in
# the relval_parameters_module. All the objects built have in 
# common the features described in the relval_includes_module.

print "\nPython RelVal"
 
# Istantiate the process
process = cms.Process (parameters.process_name)

# Add the Profiler Service if needed:
#if parameters.prof_service_flag:
if parameters.profiler_service_cuts!="":
    process=common.profiler_service(process,parameters.profiler_service_cuts)

# Add an empty Schedule
process.schedule=cms.Schedule()

# Enrich the process with the features described in the relval_includes_module.
process = includes.add_includes(process)
 
# Here we choose to make the process work only for one of the three steps 
# (SIM DIGI RECO) or for the whole chain (ALL)

# The Simuation:
if parameters.step == "ALL" or parameters.step =="SIM" :
    process=relval_simulation_module.simulate(process,
                                              parameters.step,
                                              parameters.evt_type,
                                              parameters.energy,
                                              parameters.evtnumber)
# The Digitisation:
if parameters.step == "ALL" or parameters.step =="DIGI" :
   process=relval_digireco_module.digitise(process,
                                           parameters.step,
                                           parameters.infile_name)
# The Reconstruction:
if parameters.step == "ALL" or parameters.step =="RECO" :
    process=relval_digireco_module.reconstruct(process,
                                               parameters.step,
                                               parameters.infile_name)
# Build an appropriate schedule                                                
                            
if parameters.step == "SIM":
    process.schedule.append(process.simulation_step)

elif parameters.step == "DIGI":
    process.schedule.append(process.digitisation_step)

elif parameters.step == "RECO":
    process.schedule.append(process.reconstruction_step)
    
else:
    process.schedule.append(process.simulation_step)
    process.schedule.append(process.digitisation_step)
    process.schedule.append(process.reconstruction_step)
                                                     
# Add the output on a root file if requested
if parameters.output_flag:
    process = common.event_output\
        (process, parameters.outfile_name, parameters.step)
    process.schedule.append(process.outpath)  
                                                                        
# Add metadata for production                                    
process = includes.add_production_info(process) 


# print to screen the config file in the old language
if parameters.dump_cfg_flag:
    print process.dumpConfig()
       
# A sober separator between the python program and CMSSW    
print "And now The Framework -----------------------------"
