#! /bin/env python

# Rel val launcher

import os
import time


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
                  "B_JETS":jet_en,"C_JETS":jet_en,
                  "ZPJJ":"",
                  "HZZEEEE":"","HZZMUMUMUMU":"",
                  "TTBAR":"",
                  "TAU":"20_420"}

                                    
for evt_type in type_energy_dict.keys():
    job_content="""
#! /bin/sh
cd /afs/cern.ch/user/d/dpiparo/scratch0/CMSSW_current
eval `scramv1 runtime -sh`
PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/d/dpiparo/scratch0/PythonRelval/py_configs
cd /afs/cern.ch/user/d/dpiparo/scratch0/PythonRelval/py_configs
mkdir """+evt_type+"""
./cmsRun.py """+evt_type+""" -s DIGI --dirout """+evt_type+"""/ --dirin """+evt_type+"""/
"""
    job_name="test_job_"+evt_type+".sh"
    job=file(job_name,"w")
    job.write(job_content)
    job.close()
    os.system("chmod +x "+job_name)
    os.system ("bsub -q 1nh "+job_name)            