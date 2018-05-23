import ROOT

import imp
import ssl
import subprocess

import json
import yaml


def queryGOClient(querytype, datatype, name, dbs_instance, json = False):
    query = querytype+" "+datatype+"="+name+" instance="+dbs_instance
    cmd = 'dasgoclient -query="%s"' % query
    if json:
       cmd += " -json" 
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    a = proc.communicate()
    return a[0]


def getfileInfos(lfnFileName, dbs_instance, onlyDBS = True):
    # This can return multiple structures for the file e.g. different services (dbs and phedex
    # We will only return the only with the infomatiron we need 
    load =queryGOClient("","file",lfnFileName, dbs_instance, json = True)
    if len(load.split(" ,")) == 2:
        ret1 = load.split(" ,")[0][2:] #remove [\n in the beginning of the returned string
        ret2 = load.split(" ,")[1][1:-3]#remove \n in the beginning and \n]\n in the end of the returned string
        json1 = json.loads(ret1)
        json2 = json.loads(ret2)
        allJSONs = [json1, json2]
        #print json.dumps(json2, sort_keys=True,indent=4, separators=(',', ': '))
    else:
        print "Fileinfo encountered something new! Check! Exiting!"
        exit()
    if not onlyDBS:
        return allJSONs
    else:
        for j in allJSONs:
            services = j["das"]["services"]
            if "dbs3:files" in services:
                return j

def parseLumis(dasetname, dbs_instance):
    files = {}
    returnQuery = queryGOClient("lumi run file","dataset",dasetname, dbs_instance)    
    for answer in returnQuery.split("\n"):
        answer_ = answer.split(" ")
        if len(answer_)>2:
            lfnName = answer_[0]
            run = answer_[1]
            lumis = answer_[2][1:-1]
            if not files.has_key(lfnName):
                files[lfnName] = {run : lumis.split(",") }
            else:
                files[lfnName].update({run : lumis.split(",") })
    return files
                
def getLumisInDS(dasetname, dbs_instance, countEvents = False, printOnlyResults = False):
    totalLS = 0
    nfiles = 0
    totalEvents = 0
    
    MeanLSperFile = 0

    files = parseLumis(dasetname, dbs_instance)
    
    for filename in files:
        nfiles += 1
        fileLS = 0
        LSperFile = 0
        for run in files[filename]:
            nLS = len(files[filename][run])
            totalLS += nLS
            fileLS += nLS
        if countEvents:
            fileInfos = getfileInfos(filename, dbs_instance)
            try:
                fileInfos["file"][0]["nevents"]
            except:
                print "Something went wrong with the JSON!"
                nEventsinFile = -99999999999999
            else:
                nEventsinFile = fileInfos["file"][0]["nevents"]
            totalEvents += nEventsinFile
            LSperFile = nEventsinFile/float(fileLS)
            MeanLSperFile += LSperFile
        else:
            nEventsinFile = "not Counted"
        if printOnlyResults:
            print "File {0} has {1} LS and {2} events --> Events/LS={3}".format(filename, fileLS, nEventsinFile, LSperFile)
    if countEvents and nfiles > 0:
        MeanLSperFile = MeanLSperFile/float(nfiles)
    else:
        MeanLSperFile = 0
    return totalLS, nfiles,totalEvents,MeanLSperFile, "Dataset {0} has {1} LS in {2} files and {3} events -->  Per file: Mean Events/LS {4} ".format(dasetname, totalLS, nfiles,totalEvents,MeanLSperFile)

def countLumisJSON(dasetname, dbs_instance, json):
    expandedJSON = expandJSON(json)
    files = parseLumis(dasetname, dbs_instance)
    totalLS = 0
    nfiles = 0
    for file_ in files:
        nfiles += 1
        nLSinFile = 0
        for run in files[file_]:
            if not expandedJSON.has_key(run):
                continue
            validLSinRun = expandedJSON[run]
            LSinFile = files[file_][run]
            nLS = 0
            for LS in LSinFile:
                if int(LS) in validLSinRun:
                   nLS += 1
            nLSinFile += nLS
        totalLS += nLSinFile
    print "Valid LS in Dataset {0}: {1}".format(dasetname ,totalLS) 

def expandJSON(fileName):
    with open(fileName, 'r') as f:
        LSfromFile = yaml.safe_load(f) #json loads all entries as unicode (u'..')
    expandedJSON = {}
    for run in LSfromFile:
        expandedLS = []
        for block in LSfromFile[run]:
            firstLS, secondLS = block[0], block[1]
            for i in range(firstLS, secondLS+1):
                expandedLS.append(i)
        expandedJSON[run] = expandedLS

    return expandedJSON


    
def getInfo(dasetname, dbs_instance, countEvents, printOnlyResults, splitting = None):
    infos = getLumisInDS(dasetname, dbs_instance, countEvents, printOnlyResults)
    if splitting is None:
        print infos[4]
    else:
        nJobs = infos[0]/splitting
        if infos[0]%splitting != 0:
            nJobs += 1
        events = infos[2] 
        print "{0} --> {1} jobs with splitting: {2} / ~ {3} evt per Job".format(infos[4], nJobs, splitting, events/float(nJobs))
    

if __name__ == "__main__":
    import argparse

    argumentparser = argparse.ArgumentParser(
        description='Get information about a Dataset using the DAS API'
    )

    argumentparser.add_argument(
        "--DASName",
        action = "store",
        help = "Dataset name as used in DAS",
        type=str,
        required = True,
    )
    argumentparser.add_argument(
        "--dbs",
        action = "store",
        help = "DAS dbs for the query",
        type=str,
        required = False,
        default = "prod/global"
    )

    argumentparser.add_argument(
        "--countEvents",
        action = "store_true",
        help = "Enable Event counting (WARNING: Longer runtime)",
    )
    argumentparser.add_argument(
        "--printOnlyResult",
        action = "store_false",
        help = "Disable intermediate printouts",
    )
    argumentparser.add_argument(
        "--split",
        action = "store",
        help = "Splitting for nJobs",
        type=int,
        default=None
    )
    
    argumentparser.add_argument(
        "--countValidLS",
        action = "store_false",
        help = "Disable intermediate printouts",
    )
    
    

    arguments = argumentparser.parse_args()


    getInfo(arguments.DASName, arguments.dbs, arguments.countEvents, arguments.printOnlyResult, arguments.split)
    
    if arguments.countValidLS:
        countLumisJSON(arguments.DASName, arguments.dbs, "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt")
    
    
    
