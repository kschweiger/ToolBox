import csv
from glob import glob

def getJobDiff(csvFile, SEPath, delim=";"):
    # First extract the needed information from the exported Grafana csv file
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

    #Find finished and postprocessing jobs:
    finishedJobIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["Status"] == "finished"]
    postprocessinJobIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["Status"] == "postProc" and jobInfo[_id]["ExitCode"] == 0]
    exitCodeGoodIDs = [_id for _id in jobInfo.keys() if jobInfo[_id]["ExitCode"] == 0]
    
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
    print "Files not on SE but in CSV"
    print "  - ",inCSVbutNotOnSE
    
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compare files on SE with output expected from exported Grafana stats')
    parser.add_argument('--input', action="store", required=True, help=".csv file exported from Grafana", type=str)
    parser.add_argument("--SEPath", action="store", required=True, help="Path the SE output directory. Please pass the path up to the timestemp folder **XXYYZZ_AABBCC**", type=str)
    args = parser.parse_args()

    getJobDiff(args.input, args.SEPath)
