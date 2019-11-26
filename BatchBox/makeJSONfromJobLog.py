"""
In crab logs we print the PSet. For extracte the LS the following part is relevant

== CMSSW:     lumisToProcess = cms.untracked.VLuminosityBlockRange(
== CMSSW:         "299478:140-299478:146", "299478:19-299478:19", "299478:148-299478:150", "299478:23-299478:26", "299478:61-299478:63",
== CMSSW:         "299478:147-299478:147", "299478:69-299478:75", "299478:20-299478:20", "299478:18-299478:18", "299478:114-299478:125"
== CMSSW:     ),
"""
import re

import analyzeJSON
import json

def makeJSONFromJobLog(inputFile, outputFileName):
    ### Fist find the relevant part of the log
    lumiLines = []
    with open(inputFile, "r") as f:
        lines =  f.readlines()
        parseLumis = False
        for line in lines:
            if "lumisToProcess" in line:
                parseLumis = True
                continue
            if ")," in line and parseLumis:
                break
            if parseLumis:
                lumiLines.append(line)

    lumiLineElements = []
    for line in lumiLines:
        for elem in line.split(" "):
            lumiLineElements.append(elem)
        
    #Find the lumi blocks in the relevant printput
    lumiBlocks = []
    for line in lumiLineElements:
        result = re.findall('\".+-.+\"', line)
        lumiBlocks += result


    # Format the printout and fill in dict
    lumis = {}
    for block in lumiBlocks:
        block_ = block.replace('"','')
        start, end = block_.split("-")
        run, startLS = start.split(":")
        run_, endLS = end.split(":")
        if run != run_:
            raise RuntimeError("Can be different runs in the begin and end ls? Got %"%block)
        if run not in lumis.keys():
            lumis[run] = []
        for i in range(int(startLS), int(endLS)+1):
            lumis[run].append(i)

    # Check if LS are present multiple times
    for run in lumis:
        origLen = len(lumis[run])
        lumis[run] = sorted(list(set(lumis[run])))
        if origLen != len(lumis[run]):
            raise RuntimeError("There where some double LS in run %s. Please check"%run)


    # Count for feedback in output
    nRuns = 0
    nLS = 0
    for run in lumis:
        nRuns += 1
        LSinRun = lumis[run]
        for LS in LSinRun:
            nLS += 1

    print "Extracted %s LS in %s runs"%(nLS, nRuns)

    # Use formating function from analyzeJSON module to get the json formatted for the output
    outJSON = analyzeJSON.fromatJSON(lumis)

    # Write Output file
    outputName = outputFileName+".json"
    print "Writing:",outputName
    with open(outputName, "w") as f:
        json.dump(outJSON, f)

        
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Converts lumirange part of the PSet printout to json for further processing')
    parser.add_argument('--input', action="store", required=True, help="Snippet of the JobLog", type=str)
    parser.add_argument("--output", action="store", required=True, help="Name of the output file", type=str)
    args = parser.parse_args()

    makeJSONFromJobLog(args.input, args.output)
