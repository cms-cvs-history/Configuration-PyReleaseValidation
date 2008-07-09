import sys
filename = sys.argv[1]

import pickle
result = {}
execfile(filename+".py", result)
process = result["process"]
pickleFile = open(filename+".pkl","w")
pickle.dump(process,pickleFile)
pickleFile.close()
