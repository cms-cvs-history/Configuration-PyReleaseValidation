#! /usr/bin/env python

import os
import sys


# Relevant Parameters #################################################################

cmssw_base=os.environ["CMSSW_BASE"]
cmsDriver_dir="/src/Configuration/PyReleaseValidation/data/"
perf_report_dir="~moserro/public/perfreport/"
    
IgProf_aspects=("MEM_TOTAL","PERF_TICKS")
noexec=False
#######################################################################################  

#-------------------------------

def execute(string):
    print "[execute] "+string+" ..."
    if not noexec:
        os.system (string)
    
#-------------------------------

def build_rel_val_dict(choice,nevts):

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
        #for gammaen in ("10","35"):
        #    relval_dict["GAMMA"+gammaen]="GAMMA -n"+nevts+" -e"+gammaen+" -s"       
        # Electrons
        relval_dict["E-"]="E- -n"+nevts+" -e35 -s"
    
    return relval_dict

#-------------------------    
            
def step_and_benchmark(evt, args, profiler, profiler_service_cuts, step):
    """
    Instrument the RECO step with the Profilerservice.
    Make a static report with perreport.
    """
    print "[step_and_benchmark] Entering..."
    cmsDriver_args=args #The arguments for cmsDriver
    
    profiler_line=""
    profiler_out_filename=""
    
    # The profiler is IgProf. If a profile is already present in the directory, just skip!
    if profiler is "IgProf":
        profiler_out_filename=profiler+evt+".gz"
        if os.path.exists(profiler_out_filename):
            print "[step_and_benchmark] Skipping execution of IgProf:"+\
                  "file "+profiler_out_filename+" already exists.\n"
            return 0
        profiler_line="igprof -d -t cmsRun -mp -pp -z -o "+profiler_out_filename
    
    if profiler in ("Valgrind","Patched_Valgrind"):
        profiler_out_filename=profiler+"."+evt+".out"        
        profiler_line="valgrind --tool=callgrind"
        if profiler_service_cuts is not "":              
            profiler_line+= " --combine-dumps=yes"+\
                            " --instr-atstart=no"+\
                            " --dump-instr=yes"+\
                            " --separate-recs=1"
            cmsDriver_args+="--profiler_service "+profiler_service_cuts+" "       
        
        if profiler is "Patched_Valgrind":
            profiler_line+=" --fce="+profiler_out_filename
                        
    cmsDriver_command=cmssw_base+cmsDriver_dir+"cmsDriver.py" 
    
    # Start the execution of the performance measurement procedure
  
    #Add the profiler as prefix:
    cmsDriver_args+="--prefix \""+profiler_line+"\""
    
    #Execute command
    print "[reco_and_benchmark] Running step "+step+" for "+evt+" ..."
    command=cmsDriver_command+" "+cmsDriver_args    
    if profiler=="Patched_Valgrind":# Temporary patch!
        print "[run_perfreport] Changing the envitonment for Patched Valgrind..."
        os.environ["VALGRIND_LIB"]="/afs/cern.ch/user/m/moserro/public/vgfcelib"      
    execute(command)
    
    print "[reco_and_benchmark] Making profile with "+profiler+" ..."
    
    if profiler is "Valgrind":
        # Find and Rename CallGrind Output
        # This will work only with one report file per dir
        file_list=os.listdir(".")
        search_string="callgrind.out."
    
        for file in file_list:
            if file.find(search_string)!=-1:
                print "[step_and_benchmark] Renaming "+file+" into"+\
                       profiler_out_filename+"...\n" 
                os.rename(file,profiler_out_filename)                                                  
                
    if profiler is "IgProf":
        # make igprof output readable by perftool.
        print "[reco_and_benchmark] Converting IgProf output to callgrind format..."
        for aspect in IgProf_aspects:
            perfreport_igprof_output="IgProf."+aspect+"."+evt+".out"
            IgProf_conversion_command=\
                "igprof-analyse -d -g -v -C -r "+aspect+" "+\
                   profiler_out_filename+" > "+perfreport_igprof_output
            execute(IgProf_conversion_command)
        
#---------------------------------

def make_perfreport(proclabel,profiler,step):
    """
    Make a static report with Robin Moser tool.
    https://twiki.cern.ch/twiki/bin/view/CMS/SWGuidePerfReport
    """
    
    profiler_out_filename=profiler+"."+proclabel+".out"
    reportdir=profiler_out_filename[:-4]+"_report"

    
    perfreport_command="perfreport"+\
                    " -i "+profiler_out_filename+\
                    " -d ~moserro/public/perfreport/allstandard.xml"+\
                    " -o "+reportdir  

    run_perfreport_tool(reportdir,perfreport_command)                    
#----------------------------------------------------
                    
def run_perfreport_tool(reportdir,perfreport_command):                          
    # Run perfreport
    ldlibpath=os.environ["LD_LIBRARY_PATH"]
    # Workaround for incompatibilities with CMSSW env
    os.environ["LD_LIBRARY_PATH"]="/afs/cern.ch/user/d/dpiparo/PerfSuite/perfreplibs"  
    path=os.environ["PATH"] 
    os.environ["PATH"]+=":"+perf_report_dir #Necessary to run perfreport.
    
    if not os.path.exists(reportdir):
        os.mkdir(reportdir)
    
    execute (perf_report_dir+perfreport_command)
    
    #restore the environment
    os.environ["LD_LIBRARY_PATH"]=ldlibpath
    os.environ["PATH"]=path
    
#---------------------------------

def run_edmsize(evt,step):
    """
    Run the edmsizetool and make a report with perfreporrt.
    """
    reportdir="Edm_size_report_"+evt+"_"+step
    # find the outputfile
    rootfilename=""
    file_list=os.listdir(".")
    search_string=step+".root"
    print "search_string "+search_string
    for file in file_list:
        print file
        if file.find(search_string)!=-1:
            rootfilename=file
            print "FOUND "+rootfilename
    perfreportinput=rootfilename[:-4]+"txt"
    execute("edmEventSize -o "+perfreportinput+" -d"+rootfilename)
    
    perfreport_command="perfreport -e -i "+perfreportinput+" -d "+perf_report_dir+"edmeventsize.xml -o "+reportdir
    run_perfreport_tool(reportdir,perfreport_command)

#---------------------------------

def main(argv):

    argc=len(argv)
    
    # Choose the performance profiler:
    # 1) IgProf
    # 2) Valgrind
    # 3) All
    
    profilers_dict={"1":"All",
                    "2":"IgProf",
                    "3":"Valgrind",
                    "4":"Patched_Valgrind"}
    profilers=[]
    if argv[2]=="1":
        for key in profilers_dict.keys()[1:]:
            profilers.append(profilers_dict[key])                 
    else:
        profilers=[profilers_dict[argv[2]]]    
    
    # Step to profile:
    prof_step=argv[3] 
    stepset=("SIM","DIGI","RECO","ALL")
    if prof_step not in stepset: 
        raise "Unrecognised step!"
    # Number of events:
    nevts=""
    if argc>4:
        nevts=argv[4]
    else:
        nevts="1"
    
    # Prof service cuts:
    profiler_service_cuts=""
    if argc>5:
        profiler_service_cuts=argv[5]
    else:
        profiler_service_cuts=""
             
    # The cmsDriver options to reproduce relval:
    relval_dict=build_rel_val_dict(argv[1],nevts)
    
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
        for step in stepset[:-1]:# exclude all
            if prof_step in (step,"ALL"):
                for profiler in profilers: # for each profiler,make a profile and a report
                    step_and_benchmark(evt,relval_dict[evt]+\
                        prof_step+" ",profiler,profiler_service_cuts,prof_step)
                    # make a static report
                    if profiler is "IgProf":
                       for aspect in IgProf_aspects:
                           make_perfreport(evt,profiler+"."+aspect,step)
                    else:
                       make_perfreport(evt,profiler,step)
                if prof_step=="ALL":
                    break
            else:
                cmsDriver_command=cmssw_base+cmsDriver_dir+"cmsDriver.py "+relval_dict[evt]+step
                #print cmsDriver_command # testline
                execute(cmsDriver_command)
            if step==prof_step:
                break
       
        run_edmsize(evt,step)
                                
        #come back to main directory
        os.chdir("../")       
        execute("scp -r "+evt+" lxcms118:~/localscratch/robin")
        execute("rm -r "+evt)
        #execute("rfcp -r "+evt+"/castor/cern.ch/user/d/dpiparo")
        
#------------------------------------

if __name__=="__main__":
    argc=len(sys.argv)
    usage="Usage:\n"+\
              sys.argv[0]+" <event type code> <profiler code> <step to profile>"+\
              " [nevts] [prof_serv_cuts]\n\n"+\
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
              "3. Valgrind\n"+\
              "4. Patched Valgrind\n"+\
              "Steps to profile:\n"+\
              "SIM\nDIGI\nRECO\nALL\n"
              
    if argc<4:
        print usage
        raise "Too few arguments!"
    if argc>6:
        print usage
        raise "Too many arguments!"
         
    main(sys.argv)    
    
