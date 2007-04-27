#! /usr/bin/env python

import os
import stat


for i in range(1,12):
    jobname="job_"+str(i)+".sh"
    job=open(jobname,"w")
    job.write(\
"""#! /bin/sh

pushd  /afs/cern.ch/user/d/dpiparo/scratch0/CMSSW_current
eval `scramv1 run -sh`
popd

/afs/cern.ch/user/d/dpiparo/PerfSuite/report_all_relval_v2.py """+str(i)+""" 1 15 4_14
""")
    job.close()
    os.system("chmod +rwx "+jobname)
    os.system("bsub -q 1nw "+jobname)
    
