import os
import stat
import imp
import ssl
import subprocess

def get_dataset_files(dataset, storeprefix, dbs_instance):
    das_client=imp.load_source("das_client", "/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/das_client/v02.17.04/bin/das_client.py")
    print 'getting files for',dataset
    ckey=das_client.x509()
    cert=das_client.x509()
    das_client.check_auth(ckey)
    data=das_client.get_data("https://cmsweb.cern.ch","file dataset="+dataset+" instance="+dbs_instance,0,0,0,300,ckey,cert)
    nevents=0
    size=0
    nfiles=0
    files=[]
    events_in_files=[]
    for d in data['data']:
        for f in d['file']:
            if not 'nevents' in f: continue
            files.append(storeprefix+f['name'])
            events_in_files.append(f['nevents'])
            nevents+=f['nevents']
            size+=f['size']
            nfiles+=1

    print nfiles,'files with total size',size/(1024*1024),'MB containing',nevents,'events'
    return files

def submission( scriptlist , batchsystem, logpath):
    for script in scriptlist:
        #print "Command:","bsub -q 1nh -o "+base_path+'/logs/stdout_'+str(script[-4])+" -e "+base_path+'/logs/stderr_'+str(script[-4])+" "+script
        #print "Command:","bsub -q 1nh "+script
        if batchsystem == "b":
            output = subprocess.check_output("bsub -q 1nh -o "+logpath+'/jobout_'+str(script[-4])+"_%J "+script, shell=True)
        elif batchsystem == "q":
            print "qsub -l h_vmem=4g -o "+logpath+'/jobout_'+str(script.split("/")[-1][:-3])+" -e "+logpath+'/joberr_'+str(script.split("/")[-1][:-3])+" "+script
            output = subprocess.check_output("qsub -l h_vmem=4g -o "+logpath+'/jobout_'+str(script.split("/")[-1][:-3])+" -e "+logpath+'/joberr_'+str(script.split("/")[-1][:-3])+" "+script, shell=True)
    return output


def create_script(name, cmsswbase, scriptpath, execString, envNames = None, envVals = None):
    outfilename= name
    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='cd '+cmsswbase+'/src\neval `scram runtime -sh`\n'
    script+='cd -\n'
    #script+='export X509_USER_PROXY=/afs/cern.ch/user/k/koschwei/x509up_u88606\n'
    script+='export X509_USER_PROXY=/mnt/t3nfs01/data01/shome/koschwei/.x509up_u649\n'
    if envNames is not None and envVals is not None:
        print "adding env variabels"
        for iname, name in enumerate(envNames):
            script += "export {0}={1} \n".format(name, envVals[iname])
    script+= execString+"\n"
    filename=scriptpath+'/'+outfilename
    f=open(filename,'w')
    f.write(script)
    f.close()
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

    return filename


def initialize():
    ssl._create_default_https_context = ssl._create_unverified_context
