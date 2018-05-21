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
    

def getLumisInDS(dasetname, dbs_instance, countEvents = False, printOnlyResults = False):
    returnQuery = queryGOClient("lumi run file","dataset",dasetname, dbs_instance)
    totalLS = 0
    nfiles = 0
    totalEvents = 0
    files = {}
    for answer in returnQuery.split("\n"):
        answer_ = answer.split(" ")
        if len(answer_)>2:
            lfnName = answer_[0]
            run = answer_[2]
            lumis = answer_[2][1:-1]
            if not files.has_key(lfnName):
                files[lfnName] = {run : lumis.split(",") }
            else:
                files[lfnName].update({run : lumis.split(",") })
    for filename in files:
        nfiles += 1
        for LSinRun in files[filename]:
            nLS = len(LSinRun)
            totalLS += nLS
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
        else:
            nEventsinFile = "not Counted"
        if printOnlyResults:
            print "File {0} has {1} LS and {2} events".format(filename, nLS, nEventsinFile)
    return totalLS, nfiles,totalEvents, "Dataset {0} has {1} LS in {2} files and {3} events".format(dasetname, totalLS, nfiles,totalEvents)
    
def getInfo(dasetname, dbs_instance, countEvents, printOnlyResults, splitting = None):
    infos = getLumisInDS(dasetname, dbs_instance, countEvents, printOnlyResults)
    if splitting is None:
        print infos[3]
    else:
        nJobs = infos[0]/splitting
        if infos[0]%splitting != 0:
            nJobs += 1
        print "{0} --> {1} jobs with splitting: {2}".format(infos[3], nJobs, splitting)
    

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
    

    arguments = argumentparser.parse_args()


    getInfo(arguments.DASName, arguments.dbs, arguments.countEvents, arguments.printOnlyResult, arguments.split)
    
    
