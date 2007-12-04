#! /usr/bin/env python

    
def manipulate_log(outdir,logfile_name,startevt):

    import time
    import sys
    import ROOT       
    
    os.system('pwd')
    
    # the fundamental structure: the key is the evt number the value is a list containing
    # VSIZE deltaVSIZE RSS deltaRSS
    data=[]
    values_set=('vsize','delta_vsize','rss','delta_rss')
    
    # open file and read it and fill the structure!
    logfile=open(logfile_name,'r')
    logfile_lines=logfile.readlines()
    logfile.close()

    # we get the info we need!
    i=0
    while i < len(logfile_lines):
        line=logfile_lines[i]
        if '%MSG-w MemoryCheck:' in line:
            line=line[:-1] #no \n!
            line_content_list=line.split(' ')
            event_number=int(line_content_list[-1])
            if event_number<startevt:
                i+=1
                continue
            i+=1 # we inspect the following line
            line=logfile_lines[i]
            line=line[:-1] #no \n!
            line_content_list=line.split(' ')
            vsize=float(line_content_list[4])
            delta_vsize=float(line_content_list[5])
            rss=float(line_content_list[7])
            delta_rss=float(line_content_list[8])
            
            data.append((event_number,{'vsize':vsize,
                                       'delta_vsize':delta_vsize,
                                       'rss':rss,
                                       'delta_rss':delta_rss}))
        i+=1
                                              
    # skim the second entry when the event number is the same BUG!!!!!!!
    # i take elements in couples!
    new_data=[]
    if data[0][0]==data[1][0]:
        print 'Two modules seem to have some output.\nCollapsing ...'
        i=0
        while True:
            dataline1=data[i]
            i+=1
            dataline2=data[i]
            new_eventnumber=dataline1[0]
            new_vsize=dataline2[1]['vsize']
            new_delta_vsize=dataline1[1]['delta_vsize']+dataline2[1]['delta_vsize']
            new_rss=dataline2[1]['rss']
            new_delta_rss=dataline1[1]['delta_rss']+dataline2[1]['delta_rss']
            
            new_data.append((new_eventnumber,{'vsize':new_vsize,
                                              'delta_vsize':new_delta_vsize,
                                              'rss':new_rss,
                                              'delta_rss':new_delta_rss}))
            i+=1
            if i==len(data): break
                 
        data=new_data
        print 'Collapsing: Done!'        
        
    npoints=len(data)
    
    print '%s values read and stored ...' %npoints

            
    # The Graphs 
    __argv=sys.argv # trick for a strange behaviour of the TApp..
    sys.argv=sys.argv[:1]
    ROOT.gROOT.SetStyle("Plain") # style paranoia
    sys.argv=__argv

    # Save in file
    rootfilename='%s/graphs.root' %outdir
    myfile=ROOT.TFile(rootfilename,'RECREATE')    
       
    # dictionary of graphs!
    graph_dict={}
    for value in values_set:
        graph_dict[value]=ROOT.TGraph(npoints)
        graph_dict[value].SetMarkerStyle(8)
        graph_dict[value].SetMarkerSize(.7)
        graph_dict[value].SetMarkerColor(1)
        graph_dict[value].SetLineWidth(3)
        graph_dict[value].SetLineColor(2)        
        graph_dict[value].SetTitle(value)

    
        #fill the graphs
        point_counter=0
        for event_number,vals_dict in data:
            graph_dict[value].SetPoint(point_counter,
                                       event_number,
                                       vals_dict[value])
            point_counter+=1
        
        graph_dict[value].GetXaxis().SetTitle("Event")
        last_event=data[-1][0]
        graph_dict[value].GetXaxis().SetRangeUser(0,last_event+1)
        graph_dict[value].GetYaxis().SetTitleOffset(1.3)
        graph_dict[value].GetYaxis().SetTitle("MB")
                          
        
            
        #print the graphs as files :)
        mycanvas=ROOT.TCanvas()
        mycanvas.cd()
        graph_dict[value].Draw("ALP")
    
        mycanvas.Print("%s/%s_graph.gif"%(outdir,value),"gif")

        # write it on file
        graph_dict[value].Write()
        mycanvas.Write()
        
    myfile.Close() 
        
    os.system('pwd') 
                
    # The html page!------------------------------------------------------------------------------
    
    titlestring='<b>Report executed with release %s on %s.</b>\n<br>\n<hr>\n'\
                                   %(os.environ['CMSSW_VERSION'],time.asctime())
        
    html_file_name='%s/%s.html' %(outdir,logfile_name[:-4])# a way to say the string until its last but 4th char
    html_file=open(html_file_name,'w')
    html_file.write('<html>\n<body>\n'+\
                    titlestring)
    html_file.write('<table>\n'+\
                    '<tr><td><img  src=vsize_graph.gif></img></td>'+\
                    '<td><img src=rss_graph.gif></img></td></tr>'+\
                    '<tr><td><img  src=delta_vsize_graph.gif></img></td>'+\
                    '<td><img  src=delta_rss_graph.gif></img></td></tr>' +\
                    '</table>\n')
    
    html_file.write('\n</body>\n</html>')
    html_file.close()    
    
    
#################################################################################################    
        
if __name__ == '__main__':
    
    import optparse
    import os
    
    # Here we define an option parser to handle commandline options..
    usage='simplememchecker_parser.py <options>'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--in_  profile',
                      help='The profile to manipulate' ,
                      default='',
                      dest='profile')
                      
    parser.add_option('-o', '--outdir',
                      help='The directory of the output' ,
                      default='',
                      dest='outdir')

    parser.add_option('-n', 
                      help='The event number from which we start. Default is 1.' ,
                      default='1',
                      dest='startevt')                      
                                            
    (options,args) = parser.parse_args()
    
    # Now some fault control..If an error is found we raise an exception
    if options.profile=='' or\
       options.outdir=='':
        raise('Please select a profile and an output dir!')
    
    if not os.path.exists(options.profile) or\
       not os.path.exists(options.outdir):
        raise ('Outdir or input profile not present!')
    
    try:
        startevt=int(options.startevt)        
    except ValueError:
         print 'Problems in convertng starting event value!'
         
            
    #launch the function!
    manipulate_log(options.outdir,options.profile,startevt)
    
    