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
    "/src/Configuration/PyReleaseValidation/data/relval_simulation_module.py")

#---------------------------------------------------

# Here the process is built according to the settings in
# the relval_parameters_module. All the objects built have in 
# common the features described in the relval_common_module.

print "\nPython RelVal"
 
process = cms.Process (process_name)
         
process.schedule=cms.Schedule()

# Enrich the process with the features described in the relval_includes_module.
process=common.add_includes(process)

# Add the fpe service if needed:
if fpe_service_flag:
    process.add_(common.build_fpe_service()) 

# Add the Profiler Service if needed:
if profiler_service_cuts!="":
    process.add_(common.build_profiler_service(profiler_service_cuts))

# Add the Message Logger
process.extend(common.build_message_logger())

# Set the number of events with a top level PSet
process.maxEvents=cms.untracked.PSet(input=cms.untracked.int32(evtnumber))

"""
Here we choose to make the process work only for one of the three steps 
(SIM DIGI RECO) or for the whole chain (ALL)
"""
# The Simuation:
if step in ("ALL","SIM"):
    # The random generator service    
    #process.add_(common.random_generator_service())
    # Add a flavour filter if this is the case:
    if evt_type in ("BSJPSIPHI","UDS_JETS"):
        process.flav_filter=build_filter(evt_type)
        process.flavfilter=cms.Path(process.flav_filter)
        process.schedule.append(process.flavfilter)
    # Builds the source for the process
    process.source=simulate(step,evt_type,energy,evtnumber)
    # Enrich the schedule with simulation
    process.simulation_step = cms.Path(process.psim)
    process.schedule.append(process.simulation_step)
                                              
# The Digitisation and Reconstruction:
else: # The input is a file
    process.source = common.event_input(infile_name) 
 
if step in ("ALL","DIGI","DIGIRECO"):
    process.digitisation_step=cms.Path(process.pdigi)
    process.schedule.append(process.digitisation_step)
       
if step in ("ALL","RECO","DIGIRECO"):
    if newstep3list!=[]: #add user defined elements for reco
        for element in newstep3list:
            exec("process."+element+"_step=cms.Path(process.sequences[element])")
            exec("process.schedule.append(process."+element+"_step)")
    else:
        # Choose between reconstruction algorithms.
        if evt_type in ("QCD","TTBAR"):
            process.reconstruction_step=cms.Path(process.reconstruction)
        else:
            process.reconstruction_step=cms.Path(process.reconstruction_plusRS_plus_GSF)
        process.schedule.append(process.reconstruction_step)     
        # One last item must be added to the schedule for the photon:
#        if evt_type=="GAMMA":
#            process.photonconversion=cms.Path(process.convertedPhotonSequence)
#            process.schedule.append(process.photonconversion)   
                                             
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
       
# A sober separator between the python program and CMSSW    
print "And now The Framework -----------------------------"
