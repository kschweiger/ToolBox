"""
Script for analyzing and processing a CMS lumi json file. 

k.Schweiger, 2019
"""
from __future__ import print_function

import json
import yaml


def readJSON(fileName):
    retData = None
    with open(fileName, 'r') as f:
        retData = yaml.safe_load(f)
    return retData

def expandJSON(jsondata):
    """
    In CMS lumi jsons LS a run can be (and are usually) compress by writing a range of valid 
    lumis [firstLumiinRange, lastLumiinRange] (inclusive of lastLumiinRange)
    
    This function uncompresses that for easier internal handling.

    Args:
      jsondata (dict) : CMS json lumi data (dict with run : list of LS)
    """
    LSfromFile = jsondata
    expandedJSON = {}
    for run in LSfromFile:
        expandedLS = []
        for block in LSfromFile[run]:
            firstLS, secondLS = block[0], block[1]
            for i in range(firstLS, secondLS+1):
                expandedLS.append(i)
        expandedJSON[run] = expandedLS

    return expandedJSON


def countLS(inFile):
    """
    Count the number of lumi section in lumi json
    
    Args:
       inFile (str) : Abs. path to lumi json
    """
    data = readJSON(inFile)
    data = expandJSON(data)

    nRuns = 0
    nLS = 0
    for run in data:
        nRuns += 1
        LSinRun = data[run]
        for LS in LSinRun:
            nLS += 1

    print("Found {0} run and {1} LS in {2}".format(nRuns, nLS, inFile.split("/")[-1]))

def merge(jsons):
    """
    Merge a list of CMS lumi json data

    Args:
       jsons (list) : List of CMS lumi json data (dicts with run : list of LS)
    """
    outjson = {}
    for f in jsons:
        print("Adding json form "+f+" to merge json")
        injson = jsons[f]
        for run in injson:
            if run in outjson:
                outjson[run] += injson[run]
                outjson[run] = list(set(outjson[run])) #Should not be any dublicates in the list
            else:
                outjson[run] = injson[run]
    return outjson

def fromatJSON(injson):
    """
    Format a json (in this case dict with run as key and list of lumis as element
    --> For CMS jsons we need list of json ranges. Will replace limis with [lumi, lumi]
    """
    formattedJSON = {}
    for run in injson:
        formattedJSON[run] = []
        for ls in injson[run]:
            thisLS = ls
            formattedJSON[run].append([thisLS, thisLS])

    return formattedJSON

    
def mergeJSON(workdir, inputs, outname):
    """
    Merge a list of CMS lumi jsons into one Lumi json

    Args:
       workdir (str) : Folder containing input files (abs path)
       inputs (list) : List of filenames of CMS lumi json files
       outname (str) : Filename for output file
    """
    data = {}
    for f in inputs:
        data[f] = readJSON(workdir+"/"+f)
        data[f] = expandJSON(data[f])

    mergedJSON = merge(data)
    mergedJSON = fromatJSON(mergedJSON)
    with open(workdir+"/"+outname+".json", "w") as f:
        json.dump(mergedJSON, f)
    
    
if __name__ == "__main__":
    import argparse

    argumentparser = argparse.ArgumentParser(
        description='Get information/process a CMS lumi json file'
    )

    argumentparser.add_argument(
        "--input",
        action = "store",
        help = "Input json file",
        type=str,
        nargs = "+",
        required = True
    )
    argumentparser.add_argument(
        "--count",
        action = "store_true",
        help = "Could LS in json",
    )
    argumentparser.add_argument(
        "--merge",
        action = "store_true",
        help = "Could LS in json",
    )
    argumentparser.add_argument(
        "--workdir",
        action = "store",
        help = "Directory with input files (will also be used for the output file",
        default = "."
    )
    argumentparser.add_argument(
        "--outname",
        action = "store",
        help = "Filename of the output file (pass no path or extetion)",
        default = "output"
    )

    arguments = argumentparser.parse_args()
    if arguments.count:
        for f in arguments.input:
            print("Processing file {0}/{1}".format(arguments.workdir,f))
            countLS(arguments.workdir+"/"+f)

    if arguments.merge:
        mergeJSON(arguments.workdir, arguments.input, arguments.outname)
        
