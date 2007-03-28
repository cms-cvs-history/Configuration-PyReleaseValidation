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
sys.path.append(".") # necessary to find the relval_parameters_module created by CMSdriver

# Modules to include

import FWCore.ParameterSet.Config as cms

import relval_parameters_module as parameters
import relval_common_module as common
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
     process=extend(common.build_profiler_service(parameters.profiler_service_cuts))

# Add an empty Schedule
process.schedule=cms.Schedule()

# Enrich the process with the features described in the relval_includes_module.
process=common.add_includes(process)

# Add the Message Logger
process.extend(common.build_message_logger())

"""
Here we choose to make the process work only for one of the three steps 
(SIM DIGI RECO) or for the whole chain (ALL)
"""
# The Simuation:
if parameters.step in ("ALL","SIM"):
    # The random generator service    
    process.add_(relval_simulation_module.random_generator_service())
    # Add a flavour filter if this is the case:
    if parameters.evt_type in ("BSJPSIPHI","UDS_JETS"):
        process.flav_filter=relval_simulation_module.build_filter(parameters.evt_type)
        process.flavfilter=cms.Path(process.flav_filter)
        process.schedule.append(process.flavfilter)
    # Builds the source for the process
    process.source=relval_simulation_module.simulate(parameters.step,
                                                     parameters.evt_type,
                                                     parameters.energy,
                                                     parameters.evtnumber)
    # Enrich the schedule with simulation
    process.simulation_step = cms.Path(process.psim)
    process.schedule.append(process.simulation_step)
                                              
# The Digitisation and Reconstruction:
if parameters.step in ("ALL","DIGI","RECO"):
    if not parameters.step=="ALL": # input file only if a single step is selected.
        process.source = common.event_input(parameters.infile_name)   
    if parameters.step in ("ALL","DIGI"):
        process.digitisation_step=cms.Path(process.pdigi)
        process.schedule.append(process.digitisation_step)   
    if parameters.step in ("ALL","RECO"):
        # Choose between reconstruction algorithms.
        if parameters.evt_type in ("QCD","TTBAR"):
            process.reconstruction_step=cms.Path(process.reconstruction_plusRS_plus_GSF)
        else:
            process.reconstruction_step=cms.Path(process.reconstruction)
        process.schedule.append(process.reconstruction_step)     
        # One last item must be added to the schedule for the photon:
        if parameters.evt_type=="GAMMA":
            process.photonconversion=cms.Path(process.convertedPhotonSequence)
            process.schedule.append(process.photonconversion)   
                                             
# Add the output on a root file if requested
if parameters.output_flag:
    process = common.event_output\
        (process, parameters.outfile_name, parameters.step)
    process.schedule.append(process.outpath)  
                                                                        
# Add metadata for production                                    
#process.configurationMetadata=includes.build_production_info() #Not in the 140pre1

# print to screen the config file in the old language
if parameters.dump_cfg_flag:
    print process.dumpConfig()
       
# A sober separator between the python program and CMSSW    
print "And now The Framework -----------------------------"
