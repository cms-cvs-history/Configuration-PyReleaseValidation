#! /usr/bin/env python

import os
import sys
import optparse


# Relevant Parameters #################################################################

cmssw_base=os.environ["CMSSW_BASE"]
cmsDriver_dir="/src/Configuration/PyReleaseValidation/data/"
# An empty dir assumes the tool to be installed. Please see:
#http://cmsdoc.cern.ch/~moserro/
perf_report_dir="~moserro/public/perfreport/" 
cparser =cmssw_base+"/src/Utilities/ReleaseScripts/scripts/valgrindMemcheckParser.pl" 

noexec=False
#######################################################################################  

#-------------------------------

def execute(string):
    """
    Prints a nice output. Do not execute if the noxec flag is True.
    """    
    print "[execute] "+string+" ..."
    if not noexec: # testing puroposes
        os.system (string)
    
#-------------------------------

def print_options(options):
    """
    Prints on screen the options specified in the command line.
    """
    opt_dictionary=options.__dict__
    print "\n"
    print "The relvalreport parameters |-------------"
    opt_dictionary_keys=opt_dictionary.keys()
    opt_dictionary_keys.sort()
    for key in opt_dictionary_keys:
        print key+" "+" "+str(opt_dictionary[key])
    print "-------------------------------------------"

#---------------------------------------------------------
def build_rel_val_dict(choice,nevts):
    """
    Builds a root for the cmsDriver.py commands according to the event 
    categories selected. The categories are:
    1) tau,ttbar,zee,bsjphi
    2) Jet Events
    3) Higgs Events
    4) QCD events (15/30 GeV)
    5) QCD events (30/80 GeV)
    6) QCD events (80/170 GeV)    
    7) QCD events (170/300 GeV)
    8) QCD events (300/470 GeV)
    9) QCD events (470/1000 GeV)
    10) Muon events
    11) Gamma and electron events
    12) CANDLE PROCESS
    """
    relval_dict={}
    
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

    # Our Candle -------------------------------------------------
             
    if choice=="12":
        relval_dict["CANDLE"]="QCD -n"+nevts+" -e20_30 -s" 
    
    # ------------------------------------------------------------        
             
    return relval_dict

#-------------------------    
            
def step_and_benchmark(evt, args, profiler, profiler_service_cuts, step, output_flag):
    """
    Executes the step selected in the commandline with the appropriate profiler.
    """
    print "[step_and_benchmark] Entering..."
    print "[reco_and_benchmark] Making profile with "+profiler+" ..."    
    
    cmsDriver_args=args #The arguments for cmsDriver
    
    cmsDriver_command=cmssw_base+cmsDriver_dir+"cmsDriver.py"
    
    if profiler=="":
        execute(cmsDriver_command+" "+cmsDriver_args)
    
    else:
        profiler_line=""
        profiler_out_filename=""
        
        # The profiler is IgProf. 
        if profiler.find("IgProf")!=-1:
            profiler_out_filename=profiler+"."+evt+".gz"
            profiler_line="igprof -d -t cmsRun "
            if profiler=="IgProf_perf":
                profiler_line+=" -pp"
            else:
                profiler_line+=" -mp" 
            profiler_line+=" -z -o "+profiler_out_filename
        
        # The profiler is Valgrind. 
        if profiler in ("Valgrind","Patched_Valgrind","Memcheck_Valgrind"):
            profiler_out_filename=profiler+"."+evt+".out"        
            valgrindmemcheck_out="valgrind_memcheck."+evt+".out" 
            profiler_line="valgrind "
            
            if profiler=="Memcheck_Valgrind":
                profiler_line+=" --tool=memcheck --leak-check=yes "+\
			                   " --show-reachable=yes --num-callers=20 "+\
			                   " --track-fds=yes "
            else:
                profiler_line+=" --tool=callgrind "
                
            if profiler_service_cuts!="":              
                profiler_line+= " --instr-atstart=no"#+\
                                #" --combine-dumps=yes"+\
                                #" --dump-instr=yes"+\
                                #" --separate-recs=1"
                cmsDriver_args+="--profiler_service "+profiler_service_cuts+" "       
            
            if profiler=="Patched_Valgrind":
                profiler_line+=" --fce="+profiler_out_filename 
        
        # Start the execution of the performance measurement procedure
    
        # Add the profiler as prefix:
        cmsDriver_args+="--prefix \""+profiler_line+"\""
        
        # Get Ready the command to execute
        print "[reco_and_benchmark] Running step "+step+" for "+evt+" ..."
        command=cmsDriver_command+" "+cmsDriver_args
        
        # Mute the output if required:
        if output_flag==False:
            command+=" --no_output"    
        
        if profiler=="Patched_Valgrind":# Temporary patch!
            print "[step_and_benchmark] Changing the envitonment for Patched Valgrind..."
            os.environ["VALGRIND_LIB"]="/afs/cern.ch/user/m/moserro/public/vgfcelib"      
        
        if profiler=="Memcheck_Valgrind":
            command+=" 2>&1 |tee "+valgrindmemcheck_out
        
        execute(command)
                            
        if profiler.find("IgProf")!=-1:
            # make igprof output readable by perftool.
            print "[reco_and_benchmark] Converting IgProf output to callgrind format..."
            perfreport_igprof_output=profiler+"."+evt+".out"
            IgProf_conversion_command="igprof-analyse -d -g -v -C -r "
            print "------------------"+profiler
            if profiler=="IgProf_perf":
                IgProf_conversion_command += " PERF_TICKS "
            else:
                IgProf_conversion_command += " MEM_TOTAL "         
            IgProf_conversion_command+=profiler_out_filename+" > "+perfreport_igprof_output
            execute(IgProf_conversion_command)
            
        if profiler=="Valgrind":
            # Find and Rename CallGrind Output
            # This will work only with one report file per dir
            file_list=os.listdir(".")
            search_string="callgrind.out."
        
            for file in file_list:
                if file.find(search_string)!=-1:
                    print "[step_and_benchmark] Renaming "+file+" into"+\
                        profiler_out_filename+"...\n" 
                    os.system("cp "+file+" BACKUP"+file)    
                    os.rename(file,profiler_out_filename)     
                        
#---------------------------------

def make_perfreport(proclabel,profiler,step,report_type="perfreport"):
    """
    Make a static report with Robin Moser tool.
    https://twiki.cern.ch/twiki/bin/view/CMS/SWGuidePerfReport
    """
    
    profiler_out_filename=profiler+"."+proclabel+".out"
    reportdir=profiler_out_filename[:-4]+"_report"

    if not os.path.exists(reportdir):
        os.mkdir(reportdir)    
    
    if report_type=="perfreport":
        perfreport_command="perfreport"+\
                        " -i "+profiler_out_filename+\
                        " -d ~moserro/public/perfreport/allstandard.xml"+\
                        " -o "+reportdir  
        
        run_perfreport_tool(os.path.abspath(reportdir),perfreport_command)                
    
    if report_type=="util":
        # SET PERL ENVIRONMENT:
        os.environ["PERL5LIB"]="/afs/cern.ch/user/d/dpiparo/w0/PERLlibs/5.8.0"
        valgrindmemcheck_out="valgrind_memcheck."+proclabel+".out"
        execute(cparser+" --preset +prod,-prod1 "+valgrindmemcheck_out+\
                " > "+reportdir+"/edproduce.html")
        execute(cparser+" --preset +prod1 "+valgrindmemcheck_out+\
                " > "+reportdir+"/esproduce.html")
        execute(cparser+" -t beginJob "+valgrindmemcheck_out+\
                " > "+reportdir+"/beginjob.html")        
                
#----------------------------------------------------
                    
def run_perfreport_tool(reportdir,perfreport_command):                          
    # Run perfreport
    
    ldlibpath=os.environ["LD_LIBRARY_PATH"]
    # Workaround for incompatibilities with CMSSW env
    os.environ["LD_LIBRARY_PATH"]="/afs/cern.ch/user/d/dpiparo/PerfSuite/perfreplibs"  
    os.environ["LD_LIBRARY_PATH"]+="/lib"
    path=os.environ["PATH"] 
    os.environ["PATH"]+=":"+perf_report_dir #Necessary to run perfreport.        
            
    execute (perf_report_dir+perfreport_command)
    #os.system("cd ..")
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
    print "search_string: "+search_string
    found_flag=False 
    for file in file_list:
        if file.find(search_string)!=-1:
            rootfilename=file
            print "Found "+rootfilename+" !"
            found_flag=True
    if not found_flag:
        raise ("No rootfile present!")
        
    perfreportinput=rootfilename[:-4]+"txt"
    
    if not os.path.exists(reportdir):
        os.mkdir(reportdir)    
    
    execute("edmEventSize -o "+reportdir+"/"+perfreportinput+" -d"+rootfilename)
    
    perfreport_command="perfreport -e -i "+os.path.abspath(reportdir)+"/"+perfreportinput+\
        " -d ~moserro/public/perfreport/edmeventsize.xml -o "+ os.path.abspath(reportdir)
    run_perfreport_tool(os.path.abspath(reportdir),perfreport_command)

#---------------------------------

def principal(typecode,options):
 
    print_options(options)
                        
    profiler=options.profiler
    
    # Step to profile:
    stepset=("SIM","DIGI","RECO","ALL","")
    if options.prof_step not in stepset: 
        raise "Unrecognised step!"
        
    # Number of events:
    nevts=options.number
    
    # Prof service cuts:
    profiler_service_cuts=options.profiler_service_cuts
    
    #Turn off the output
    output_flag=not options.no_output_flag
        
    # The cmsDriver options to reproduce relval:
    relval_dict=build_rel_val_dict(typecode,nevts)
    
    # Loop on the event types
    os.chdir(options.dirout)    
    for evt in relval_dict:
        # If doesn't exist make a evttype dir
        if not os.access(evt,os.F_OK):
            print "[main] Creating directory "+evt+"..."
            os.mkdir(evt)
        # and enter it
        os.chdir(evt)

        if options.prof_step!="":
            step_and_benchmark(evt,relval_dict[evt]+\
                options.prof_step+" ",profiler,profiler_service_cuts,options.prof_step,output_flag)
        
        #make a static report
        if options.profiler!="":
            make_perfreport(evt,profiler,options.prof_step)
        
        # Run Utility perl scripts if requested
        if profiler=="Memcheck_Valgrind":
            make_perfreport(evt,profiler,options.prof_step,"util")  
            
        # Prepare an eventsize report if requested
        if options.edm_size_flag:  
            run_edmsize(evt,options.prof_step)
                                
        #come back to main directory
        os.chdir("../")
        
#------------------------------------

if __name__=="__main__":
  
    if len(sys.argv) < 2:
        raise ("Too few arguments!")
  
        
    event_codes="1.  tau,ttbar,zee,bsjphi\n"+\
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
                "12. Standard Candle\n"
          
    usage="%prog <TYPECODE> [options].\n\n"+\
          "The supported event codes are:\n"+event_codes+"\n"+\
          "Examples:\n"+\
          "relvalreport.py 12 -d CMSSW_140_Reports/ -n100 -p2 -sALL -e\n"+\
          "relvalreport.py 12 -d CMSSW_140_Reports/ -n13 -p3 -sALL --profiler_service=2_12\n"

    parser = optparse.OptionParser(usage)

    parser.add_option("-p", "--profiler",
                      help="Profilers are: IgProf_mem, IgProf_perf, "+\
                           "Valgrind, Patched Valgrind, Memcheck_Valgrind.",
                      default="",
                      dest="profiler")

    parser.add_option("-s", "--step",
                      help="The steps are: ALL,SIM,DIGI,RECO.",
                      default="",
                      dest="prof_step")
                      
    parser.add_option("-n", "--number",
                      help="The number of evts. The default is 1.",
                      default="1",
                      dest="number")  
                      
    parser.add_option("--profiler_service",
                      help="Equip the process with the profiler service "+\
                           "by Vincenzo Innocente. First and the last events in "+\
                           " the form <first>_<last>.",
                      default="",
                      dest="profiler_service_cuts")                      
                      
    parser.add_option("--no_output",
                      help="Do not write anything to disk.",
                      action="store_true",
                      default=False,
                      dest="no_output_flag")                                             

    parser.add_option("-d","--dirout",
                      help="The outfile directory.",
                      default="",
                      dest="dirout") 
                      
    parser.add_option("-e","--edm_size",
                      help="Make an EDM Size Report.",
                      action="store_true",
                      default=False,
                      dest="edm_size_flag")                      

    (options,args) = parser.parse_args()                           
    
    # FAULT CONTROL
    if options.dirout=="":
        raise ("Specify at least one output directory!")                          
    
    prof_set=("IgProf_mem",
              "IgProf_perf",
              "Valgrind",
              "Patched_Valgrind",
              "Memcheck_Valgrind",
              "")
        
    if not options.profiler in prof_set:
        raise ("Profiler not Recognised")
    
    if not os.path.exists(cparser) and options.profiler=="Memcheck_Valgrind":
        print cparser + " does not exist please check.\n"
        raise("ValGrindMemcheckParser not found!")
        

    
                                         
    principal(sys.argv[1],options)    
    
