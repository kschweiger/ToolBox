import ROOT

import imp
import ssl
import subprocess

import json
import yaml
import copy


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
    load = load.replace("[\n","")
    load = load.replace("\n]\n","")
    allJSONs = []
    for j in load.split(" ,"):
        allJSONs.append(json.loads(j))

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


def genMCJSON(dasetname, dbs_instance, outputName):
    print "RUNNING genMCJSON"
    files = parseLumis(dasetname, dbs_instance)
    lumis4Json = {}
    for file_ in files:
        #print files[file_]
        for run in  files[file_]:
            if not lumis4Json.has_key(run):
                lumis4Json[run] = []
            intList = []
            for ls in files[file_][run]:
                intList.append([int(ls),int(ls)])
            lumis4Json[run] += intList
            #print lumis4Json

    print "Validating:"
    total = 0
    for run in lumis4Json:
        for ls in lumis4Json[run]:
            total += ls[1]-ls[0]+1
    print "Found {0} ls in the output data".format(total)
    
    with open(outputName+'.json', 'w') as outfile:
        json.dump(lumis4Json, outfile)

    return lumis4Json

def genSplitMCJSON(dasetname, dbs_instance, outputName, nLSperJob):
    maxLS = 10000*nLSperJob
    lumis4Json = genMCJSON(dasetname, dbs_instance, outputName)
    total = 0
    allLS = []
    thisLS = []
    for run in lumis4Json:
        for ls in lumis4Json[run]:
            thisL = ls[0]
            total += 1
            thisLS.append([thisL, thisL])  
            if total == maxLS-100:
                allLS.append({run : copy.copy(thisLS)})
                thisLS = []
                total = 0
    allLS.append({run : copy.copy(thisLS)})
    print "------------------------------------------------"
    for iData, data in enumerate(allLS):
        print "Validating:"
        total = 0
        for run in data:
            for ls in data[run]:
                total += ls[1]-ls[0]+1
        print "Found {0} ls in the output data".format(total)
        with open(outputName+"_"+str(iData)+'.json', 'w') as outfile:
            json.dump(data, outfile)


    
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
    argumentparser.add_argument(
        "--genJSON",
        action = "store_true",
        help = "Disable intermediate printouts",
    )
    argumentparser.add_argument(
        "--LSperJob",
        action = "store",
        type = int,
        help = "Cacluate the JSON files for large jobs where the 10k limit is passed",
        default = None,
    )
    
    
    
    
    arguments = argumentparser.parse_args()

    if not arguments.genJSON:
        getInfo(arguments.DASName, arguments.dbs, arguments.countEvents, arguments.printOnlyResult, arguments.split)
    
        if arguments.countValidLS:
            countLumisJSON(arguments.DASName, arguments.dbs, "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt")
    else:
        fileName = "SplitJSON_"+arguments.DASName.split("/")[1].split("-")[0]
        print fileName
        if arguments.LSperJob is None:
            genMCJSON(arguments.DASName, arguments.dbs, fileName)
        else:
            genSplitMCJSON(arguments.DASName, arguments.dbs, fileName, arguments.LSperJob)
            
