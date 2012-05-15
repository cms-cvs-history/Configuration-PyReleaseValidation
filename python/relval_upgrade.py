
# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = {}

# each workflow defines a name and a list of steps to be done. 
# if no explicit name/label given for the workflow (first arg),
# the name of step1 will be used

workflows[3000] = ['', ['SingleMuPt10UPG','RECOUPG']]
workflows[3001] = ['', ['SingleMuPt100UPG','RECOUPG']]
workflows[3002] = ['', ['SingleMuPt1000UPG','RECOUPG']]

workflows[3003] = ['', ['MinBiasUPG8','RECOUPG']]


workflows[3100] = ['', ['MinBiasUPG14','RECOUPG']]


#workflows[3200] = ['','MinBiasUPG8','RECOUPGPU']]



                   
