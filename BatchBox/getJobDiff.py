import csv
from glob import glob

def parseCSV(csvFile, delim):
    jobInfo ={}
    indices={"Id" : -99, "ExitCode" : -99, "Status" : -99}
    with open(csvFile, 'rb') as f_csv:
        rows = csv.reader(f_csv, delimiter=delim)
        header = rows.next()
        for key in indices:
            indices[key] = header.index(key)
        keepProcessing = True
        while keepProcessing:
            try:
                thisRow = rows.next()
                ID = int(thisRow[indices["Id"]])
                try:
                    ExitCode = int(thisRow[indices["ExitCode"]])
                except ValueError:
                    ExitCode = -1 # For pending jobs
                Status = thisRow[indices["Status"]]
                jobInfo[ID] = {"Status" : Status, "ExitCode" : ExitCode}
            except StopIteration:
                keepProcessing = False

    return jobInfo

def parseCrabLog(crabLog):
    statusLines = []
    jobInfo ={}
    with open(crabLog, "r") as f:
        lines = f.readlines()
        captureLines = False
        for line in lines:
            if "Extended Job Status Table:" in line:
                captureLines = True
                continue
            if "Summary of run jobs" in line and captureLines:
                break
            if captureLines:
                _line = [l for l in line.split(" ") if l != ""]
                _line[-1] = _line[-1].replace("\n","")
                if len(_line) > 1:
                    statusLines.append(_line)

    jobStatus = statusLines[1::]
    for line in jobStatus:

        ID = int(line[0])
        ExitCode = int(line[9])
        Status = line[1]
        jobInfo[ID] = {"Status" : Status, "ExitCode" : ExitCode}
        
    return jobInfo


def getJobDiff(inFile, SEPath, isCrabLog, delim=";"):
    # First extract the needed information from the exported Grafana csv file
    if not isCrabLog:
        jobInfo = parseCSV(inFile, delim)
    else:
        jobInfo = parseCrabLog(inFile)
    
    #Find finished and postprocessing jobs:
    finishedJobIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["Status"] == "finished"]
    runningJobIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["Status"].lower() == "running"]
    postprocessinJobIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["Status"] == "postProc" and jobInfo[_id]["ExitCode"] == 0]
    exitCodeGoodIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["ExitCode"] == 0]
    
    print "Found %s jobs in Running"%(len(runningJobIDs))
    print "Found %s jobs in finished"%(len(finishedJobIDs))
    print "Found %s jobs in postProc"%(len(postprocessinJobIDs))
    print "  Sum = %s"%(len(finishedJobIDs)+len(postprocessinJobIDs))
    print "  (Found %s with exitcode = 0)"%(len(exitCodeGoodIDs))
    
    # Second get files present on the FS
    fileIDsSE = []
    folders = glob(SEPath+"/*")
    for folder in folders:
        rFiles = glob(folder+"/*.root")
        for rFile in rFiles:
            fileName = rFile.split("/")[-1]
            fileName = fileName.replace(".root","")
            prefix, thisFileID = fileName.split("_")
            fileIDsSE.append(int(thisFileID))

    print "Found %s files on the FS"%(len(fileIDsSE))


    #Get the difference
    #new set with elements in s but not in t --> s.difference(t)
    inCSVbutNotOnSE = list(set(exitCodeGoodIDs).difference(set(fileIDsSE)))
    onSEbutNotInCSV = list(set(fileIDsSE).difference(set(exitCodeGoodIDs)))

    print "Files not in CSV but on SE"
    print "  - ",onSEbutNotInCSV
    for onSEId in onSEbutNotInCSV:
        print "     Status according to CSV for %s is %s"%(onSEId, jobInfo[onSEId]["Status"])
    print "Files not on SE but in CSV"
    print "  - ",inCSVbutNotOnSE
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compare files on SE with output expected from exported Grafana stats')
    parser.add_argument('--input', action="store", required=True, help=".csv file exported from Grafana", type=str)
    parser.add_argument("--SEPath", action="store", required=True, help="Path the SE output directory. Please pass the path up to the timestemp folder **XXYYZZ_AABBCC**", type=str)
    parser.add_argument("--isCrabLog", action="store_true", help="If passed the input file will be interpreted as log file from crab status --long")
    args = parser.parse_args()

    getJobDiff(args.input, args.SEPath, args.isCrabLog)
