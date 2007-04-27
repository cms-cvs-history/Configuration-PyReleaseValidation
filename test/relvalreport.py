#! /usr/bin/env python

import os
import sys


# Relevant Parameters #################################################################

cmssw_base=os.environ["CMSSW_BASE"]
cmsDriver_dir="/src/Configuration/PyReleaseValidation/data/"

#######################################################################################   
        
def reco_and_benchmark(evt, args, profiler, cmssw_base, profiler_service_cuts):
    """
    Instrument the RECO step with the Profilerservice.
    Make a static report with perreport.
    """
    print "[reco_and_benchmark] Entering..."
    cmsDriver_args=args #The arguments for cmsDriver
    
    profiler_line=""
    profiler_out_filename=""
    
    if profiler == "Valgrind":
        profiler_line="valgrind --tool=callgrind"+\
                      " --combine-dumps=yes"+\
                      " --instr-atstart=no"+\
                      " --dump-instr=yes"+\
                      " --separate-recs=1"
    
    if profiler=="IgProf":
        profiler_out_filename="igprof."+evt+".gz"
        profiler_line="igprof -d -t cmsRun -mp -z -o "+profiler_out_filename
                        
    cmsDriver_command=cmssw_base+cmsDriver_dir+"cmsDriver.py" 
    
    # Start the execution of the performance measurement procedure
   
    #ProfilerService:
    cmsDriver_args+="--profiler_service "+profiler_service_cuts+" "
  
    #Add the profiler as prefix:
    cmsDriver_args+="--prefix \""+profiler_line+"\""
    
    #Execute command
    print "[reco_and_benchmark] Running RECO step for "+evt+" ..."
    command=cmsDriver_command+" "+cmsDriver_args
    print command # testline
    os.system(command)
    
    print "[reco_and_benchmark] Making profile with "+profiler+" ..."
    
    if profiler=="Valgrind":
        # Find and Rename CallGrind Output
        # This will work only with one report file per dir
        profiler_out_filename=profiler+"."+evt+".out"
        file_list=os.listdir(".")
        search_string="callgrind.out."
    
        for file in file_list:
            if file.find(search_string)!=-1:
                print file
                os.rename(file,profiler_out_filename)                            
    
    if profiler=="IgProf":
        perfreport_igprof_output="IgProf."+evt+".out"
        # make igprof output readable by perftool.
        print "[reco_and_benchmark] Converting IgProf output to callgrind format..."
        IgProf_conversion_command=\
           "igprof-analyse -d -g -v -C -r MEM_TOTAL "+profiler_out_filename+" > "+perfreport_igprof_output
        os.system(IgProf_conversion_command)
        
#---------------------------------

def run_perfreport(proclabel,profiler):
    """
    Make a static report with Robin Moser tool.
    https://twiki.cern.ch/twiki/bin/view/CMS/SWGuidePerfReport
    """
    
    profiler_out_filename=profiler+"."+proclabel+".out"
    reportdir=proclabel+"_"+profiler+"_report"

    
    perf_report_dir="~moserro/public/perfreport"
    perfreport_command=perf_report_dir+"/perfreport"+\
                    " -i "+profiler_out_filename+\
                    " -d ~moserro/public/perfreport/allstandard.xml"+\
                    " -o "+reportdir  
            
    # Run perfreport
    ldlibpath=os.environ["LD_LIBRARY_PATH"]
    # Workaround for incompatibilities with CMSSW env
    os.environ["LD_LIBRARY_PATH"]="/afs/cern.ch/user/d/dpiparo/PerfSuite/perfreplibs"
    
    path=os.environ["PATH"] 
    os.environ["PATH"]+=":"+perf_report_dir #Necessary to run perfreport.
    
    if not os.access(reportdir,os.F_OK):
        os.mkdir(reportdir)
    
    print perfreport_command # testline
    os.system (perfreport_command)
    
    #restore the environment
    os.environ["LD_LIBRARY_PATH"]=ldlibpath
    os.environ["PATH"]=path

#---------------------------------

def main(argv):

    argc=len(argv)
    
    # Number of events:
    nevts=""
    if argc>3:
        nevts=argv[3]
    else:
        nevts="1"
    # Prof service cuts:
    profiler_service_cuts=""
    if argc>4:
        profiler_service_cuts=argv[4]
    else:
        profiler_service_cuts="3_13"
        
    # Choose the performance profiler:
    # 1) IgProf
    # 2) Valgrind
    # 3) All
    
    profilers_dict={"1":"All",
                    "2":"IgProf",
                    "3":"Valgrind"}
    profilers=[]
    if argv[2]=="1":
        for key in profilers_dict.keys()[1:]:
            profilers.append(profilers_dict[key])                 
    else:
        profilers=[profilers_dict[argv[2]]]
     
    # The cmsDriver options to reproduce relval:
    relval_dict={}
    
    #Build the dictionary according to the choice in the commandline:
    # 1) tau,ttbar,zee,bsjphi
    # 2) Jet Events
    # 3) Higgs Events
    # 4) QCD events (15/30 GeV)
    # 5) QCD events (30/80 GeV)
    # 6) QCD events (80/170 GeV)    
    # 7) QCD events (170/300 GeV)
    # 8) QCD events (300/470 GeV)
    # 9) QCD events (470/1000 GeV)
    # 10) Muon events
    # 11) Gamma and electron events

    
    choice=argv[1]
    
    fix_energy_evts={"1":("TAU","TTBAR","ZEE","BSJPSIPHI"),
                     "2":("ZPJJ","B_JETS","C_JETS","UDS_JETS"),
                     "3":("HZZEEEE","HZZMUMUMUMU")}
    
    if choice in ("1","2","3"): # Fixed energy evts
        for el in fix_energy_evts[choice]:
            relval_dict[el]=el+" -n"+nevts+" -s" 
    
    #QCD
    qcd_evts={"4":("15_20","20_30"),
              "5":("30_50","50_80"),           
              "6":("80_120","120_170"),
              "7":("170_230","230_300"),
              "8":("300_380","380_470"),
              "9":("470_600","600_800","800_1000")}
                 
    if choice in ("4","5","6","7","8","9"): # QCD evts
        for qcden in qcd_evts[choice]:
            relval_dict["QCD"+qcden]="QCD -n"+nevts+" -e"+qcden+" -s"        
    
    if choice=="10": # Muons evts
        for sign in ("+","-"):
            for muen in ("1","10","100"):
                relval_dict["MU"+sign+muen]="MU"+sign+" -n"+nevts+" -e"+muen+" -s"
        relval_dict["10MU"]="10MU- -n"+nevts+" -e1_10 -s"
    
    if choice=="11": # Gamma and Electrons evt
        for gammaen in ("10","35"):
            relval_dict["GAMMA"+gammaen]="GAMMA -n"+nevts+" -e"+gammaen+" -s"       
        # Electrons
        relval_dict["E-"]="E- -n"+nevts+" -e35 -s"

    # Loop on the event types
    os.chdir("/tmp/")    
    for evt in relval_dict:
        print evt
        # If doesn't exist make a evttype dir
        if not os.access(evt,os.F_OK):
            print "[main] Creating directory "+evt+"..."
            os.mkdir(evt)
        # and enter it
        os.chdir(evt)
        
        # Loop on the steps
        for step in ("SIM","DIGI"):
            cmsDriver_command=cmssw_base+cmsDriver_dir+"cmsDriver.py "+relval_dict[evt]+step
            print cmsDriver_command # testline
            os.system(cmsDriver_command)
    
        for profiler in profilers: # for each profiler run reco,make a profile and a report
            # Reconstruction with perfmeasurement
            #set_CMSSW_env(cmssw_env)
            reco_and_benchmark(evt,relval_dict[evt]+"RECO ",profiler,cmssw_base,profiler_service_cuts)
            # make a static report
            run_perfreport(evt,profiler)    
                
        #come back to main dir
        os.chdir("../")       
        os.system("scp -r "+evt+" lxcms118:~/localscratch")
        #os.system("rfcp -r "+evt+"/castor/cern.ch/user/d/dpiparo")
        
#------------------------------------

if __name__=="__main__":
    argc=len(sys.argv)
    usage="Usage:\n"+\
              sys.argv[0]+" <event type code> <profiler code> [nevts] [prof_serv_cuts]\n\n"+\
              "Event codes:\n"+\
              "1.  tau,ttbar,zee,bsjphi\n"+\
              "2.  Jet Events\n"+\
              "3.  Higgs Events\n"+\
              "4.  QCD events (15/30 GeV)\n"+\
              "5.  QCD events (30/80 GeV)\n"+\
              "6.  QCD events (80/170 GeV)\n"+\
              "7.  QCD events (170/300 GeV)\n"+\
              "8.  QCD events (300/470 GeV)\n"+\
              "9.  QCD events (470/1000 GeV)\n"+\
              "10. Muon events\n"+\
              "11. Gamma and electron events\n"+\
              "Profiler codes:\n"+\
              "1. All\n"+\
              "2. IgProf\n"+\
              "3. Valgrind\n"
    if argc<3:
        print usage
        raise "Too few arguments!"
    if argc>5:
        print usage
        raise "Too many arguments!"
         
    main(sys.argv)    
    
