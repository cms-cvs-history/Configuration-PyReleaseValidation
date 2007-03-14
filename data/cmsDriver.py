#! /usr/bin/python

# A Pyrelval Wrapper

import optparse
import sys
import os

def print_options(options):
    opt_dictionary=options.__dict__
    print "\n"
    print "The configuration parameters |-------------"
    opt_dictionary_keys=opt_dictionary.keys()
    opt_dictionary_keys.sort()
    for key in opt_dictionary_keys:
        print key+" "+" "+str(opt_dictionary[key])
    print "-------------------------------------------"


# The supported evt types and default energies:
qed_ene="10"
jet_en="50_120"
type_energy_dict={"MU+":qed_ene,
                  "MU-":qed_ene,
                  "E+":qed_ene,
                  "E-":qed_ene,
                  "GAMMA":qed_ene,
                  "10MU+":qed_ene,
                  "10MU-":qed_ene,
                  "10E+":qed_ene,
                  "10E-":qed_ene,
                  "10GAMMA":qed_ene,
                  "QCD":"380_470",
                  "B_JETS":jet_en,"C_JETS":jet_en,"UDS_JETS":jet_en,
                  "B_JPSIPHI":"",
                  "ZPJJ":"",
                  "HZZEEEE":"","HZZMUMUMUMU":"",
                  "TTBAR":"",
                  "TAU":"20_420"}

# Sorted list of available types for the user help.
types_list=type_energy_dict.keys()
types_list.sort()

# Prepare a parser to read the options
usage=\
"""%prog <TYPE> [options].
The supported event types are: """+str(types_list)+""".
Examples:
cmsRun.py QCD
cmsRun.py 10MU+ -e 45 -n 100 --no_output
cmsRun.py B_JETS -s DIGI -e 40_130 -n 50 --filein MYSIMJETS --fileout MYDIGIJETS
"""
parser = optparse.OptionParser(usage)

# Options of the script
#parser.add_option("",
                   #help="The type of the event(s) selected. "+\
                        #"The currently available types are:\n"+\
                        #str(types_list),
                   #dest="evt_type")

parser.add_option("-s", "--step",
                   help="The desired step. The possible values are: "+\
                        "SIM (Simulation), "+\
                        "DIGI (Digitisation), "+\
                        "RECO (Reconstruction), "+\
                        "ALL (Simulation-Reconstruction-Digitisation).",
                   default="ALL",
                   dest="step")

parser.add_option("-n", "--number",
                   help="The number of evts. The default is 1.",
                   default="1",
                   dest="number")

parser.add_option("-e", "--energy",
                   help="The event energy. If absent, a default value is "+\
                         "assigned according to the event type.",
                   dest="energy") 

parser.add_option("--filein",
                   help="The infile name. If absent and necessary a "+\
                        "default value is assigned. "+\
                        "The form is <type>_<energy>_<step>.root.",
                   default="",
                   dest="filein")

parser.add_option("--fileout",
                   help="The outfile name. If absent a default value is "+\
                        "assigned. The form is <type>_<energy>_<step>.root.",
                   default="",
                   dest="fileout")
                   
parser.add_option( "--dirin",
                   help="The infile directory. If absent the default value ./ is "+\
                        "assigned.",
                   default="",
                   dest="dirin")                    

parser.add_option( "--dirout",
                   help="The outfile directory. If absent the default value ./ is "+\
                        "assigned.",
                   default="",
                   dest="dirout")                
                   
parser.add_option("--no_output",
                  help="Do not write anything to disk. This is for "+\
                       "benchmarking purposes.",
                  action="store_true",
                  default=False,
                  dest="no_output_flag")

parser.add_option("--dump",
                  help="Dump the config file in the old config "+\
                       "language. It is printed on stdout.",
                  action="store_true",
                  default=False,
                  dest="dump_cfg_flag")

parser.add_option("--silent",
                  help="Do not write on screen the info about the "+\
                       "Python configuration building action by "+\
                       "PyRelVal.",
                  action="store_false",
                  default=True,
                  dest="dbg_flag")

parser.add_option("--prefix",
                  help="Specify a prefix to the cmsRun command.",
                  default="",
                  dest="prefix")                                    
                  

(options,args) = parser.parse_args() # by default the arg is sys.argv[1:]

# A simple check on the consistency of the arguments
if len(sys.argv)==1:
    raise "Event Type: ", "No event type specified!"

options.evt_type = sys.argv[1]

if not options.evt_type in type_energy_dict.keys():
    raise "Event Type: ","Unrecognised event type."

if options.energy==None:
  options.energy=type_energy_dict[options.evt_type]

# Build the IO files if necessary.
# The default form of the files is:
# <type>_<energy>_<step>.root
prec_step = {"ALL":"","SIM":"","DIGI":"SIM","RECO":"DIGI"}

if options.filein=="" and not options.step in ("ALL","SIM"):
    options.filein=options.evt_type+"_"+options.energy+\
    "_"+prec_step[options.step]+".root"

if options.fileout=="":
    options.fileout=options.evt_type+"_"+options.energy+"_"+options.step+".root"

if options.prefix == None:
    options.prefix=""

# Print the options to screen
print_options(options)

cfgfile="""
#############################################################
#                                                           #
#              relval_parameters_module                     #
#                                                           #
#  This module contains a dictionary in which               #
#  the parameters relevant for the process are stored.      #
#  The parameters are:                                      #
#   - Type of the events          (string)                  #
#   - Number of the events        (int)                     # 
#   - Energy of the events        (string)                  #
#   - input and output files      (string)                  #
#   - Step: SIM DIGI RECO ALL     (string)                  #
#  The supported types are:                                 #
#   - QCD (energy in the form min_max)                      #
#   - B_JETS, C_JETS (energy in the form min_max for cuts)  #
#   - TTBAR                                                 #
#   - MU+,MU-,E+,E-,GAMMA,10MU+,10E-...                     #
#   - TAU (energy in the form min_max for cuts)             #
#   - HZZEEEE, HZZMUMUMUMU                                  #
#   - ZEE (no energy is required)                           #
#   - ZPJJ: zee prime in 2 jets                             #
#                                                           #
#############################################################

# Process Parameters

# The name of the process
process_name='""" +options.step+ """'
# The type of the process. Please see the complete list of 
# available processes.
evt_type='"""+options.evt_type+"""'
# The energy in GeV. Some of the tipes require an
# energy in the form "Emin_Emax"
energy='"""+options.energy+"""'
# Number of evts to generate
evtnumber="""+options.number+"""
# Input and output file names
infile_name='"""+options.dirin+options.filein+"""'
outfile_name='"""+options.dirout+options.fileout+"""'
# The step: SIM DIGI RECO and ALL to do the 3 in one go.
step='"""+options.step+"""'
# Omit the output in a root file
output_flag= """+str(not options.no_output_flag)+"""

# Pyrelval parameters
# Enable verbosity
dbg_flag=True
# Dump the oldstyle cfg file.
dump_cfg_flag="""+str(options.dump_cfg_flag)+"""
"""

#print cfgfile # Test line!

# Write down the configuration in a Python module
config_module=file("./relval_parameters_module.py","w")
config_module.write(cfgfile)
config_module.close()

# Prepare command execution
command=options.prefix+\
" cmsRun $CMSSW_BASE/src/Configuration/PyReleaseValidation/data/relval_main.py"
print "Launching "+command+"..."
sys.stdout.flush() 
print os.system(command) # And Launch the Framework!
