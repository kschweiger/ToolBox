import os

import ScriptHandling

def resubmit(scripts, jobnames, ask = True):
    for reason, name in jobnames:
        script = scripts.scriptsDict[name]
        errorfile = script.errpath+"/"+script.errfilename
        logfile = script.logpath+"/"+script.logfilename
        do = True
        if ask:
            do = False
            a = raw_input("Should job {0} ( {1} ) be resubmitted? [y/n]".format(name, reason))
            if a == "y":
                do = True
        if do:
            os.remove(errorfile)
            os.remove(logfile)
            print "Resubmitting job {0}".format(name)
            script.submit(scripts.system)


def checkJobs(scriptlist):
    import subprocess
    checks = {}

    print "Success keys:"
    for ikey, key in enumerate(scriptlist.successKeys):
        print ikey, key
    print "Fail keys:"
    for ikey, key in enumerate(scriptlist.failKeys):
        print ikey, key

    for script in scriptlist.scripts:
        #print script.printScriptInfo()
        checks[script.name] = {}
        #Check if job is still runnign:
        checks[script.name]["isRunning"] = False
        checks[script.name]["isQueued"] = False
        #if "Batch" in script.name:
        #print "------",script.batchID, script.name
        #print "------","1" in subprocess.check_output('qstat | grep "'+script.batchID+'" | grep " r " | wc -l', shell=True)
        if "1" in subprocess.check_output('qstat | grep "'+script.batchID+'" | grep " r " | wc -l', shell=True):
            checks[script.name]["isRunning"] = True
        if "1" in subprocess.check_output('qstat | grep "'+script.batchID+'" | grep " qw " | wc -l', shell=True):
            checks[script.name]["isQueued"] = True

        #Check if oputfile is written:
        #print "Checking for",script.outpath+"/"+script.outfilename
        checks[script.name]["hasOutput"] = os.path.isfile(script.outpath+"/"+script.outfilename)
        #Check for log and error file
        checks[script.name]["hasLog"] = os.path.isfile(script.logpath+"/"+script.logfilename)
        checks[script.name]["hasErr"]= os.path.isfile(script.errpath+"/"+script.errfilename)
        #Check for sucresskeys
        lines = None
        if checks[script.name]["hasLog"]:
            with open(script.logpath+"/"+script.logfilename, "r") as f:
                read_data = f.read()
                lines = read_data.split("\n")
        for ikey, key in enumerate(scriptlist.successKeys):
            checks[script.name]["hasSucesskey_{0}".format(ikey)] = False
            if lines is not None:
                for line in lines:
                    if key in line:
                        checks[script.name]["hasSucesskey_{0}".format(ikey)] = True
        lines = None
        if checks[script.name]["hasErr"]:
            with open(script.errpath+"/"+script.errfilename, "r") as f:
                read_data = f.read()
                lines = read_data.split("\n")
        for ikey, key in enumerate(scriptlist.failKeys):
            checks[script.name]["hasFailkey_{0}".format(ikey)] = False
            if lines is not None:
                for line in lines:
                    if key in line:
                        checks[script.name]["hasFailkey_{0}".format(ikey)] = True

    return checks

def findfinishedJobs(checks):
    finishedJobs = []
    for jobname in checks:
        currentJob = checks[jobname]
        if not currentJob["isRunning"] and not currentJob["isQueued"]:
            finishedJobs.append(jobname)

    return finishedJobs

def findFailedJobs(scripts, finishedJobs, checks):
    errormsgs = ["*** Break *** segmentation violation"]

    failedJobs = []
    onlynames = []
    wasappended = False
    for jobname in finishedJobs:
        wasappended = False
        currentJob = checks[jobname]
        script = scripts.scriptsDict[jobname]
        if not currentJob["hasOutput"]:
            if not wasappended:
                failedJobs.append(("hasOutput", jobname))
                onlynames.append(jobname)
                wasappended = True
                break
        if currentJob["hasErr"]:
            lines = None
            with open(script.errpath+"/"+script.errfilename, "r") as f:
                read_data = f.read()
                lines = read_data.split("\n")
            for errmsg in errormsgs:
                for line in lines:
                    if errmsg in line:
                        if not wasappended:
                            failedJobs.append(("hasErr", jobname))
                            onlynames.append(jobname)
                            wasappended = True
                            break
        for iFkey in range(len(scripts.failKeys)):
            if currentJob["hasFailkey_{0}".format(iFkey)] is True:
                if not wasappended:
                    failedJobs.append(("hasFailkey_{0}".format(iFkey), jobname))
                    onlynames.append(jobname)
                    wasappended = True
                    break

    return failedJobs, onlynames

def showJobInfo(scripts, checks, finishedJobs, failedJobs):
    nrunning = 0
    nqueued = 0
    nfinished = 0
    nfailed = 0
    for namekey in checks:
        if checks[namekey]["isRunning"] is True:
            nrunning += 1
        if checks[namekey]["isQueued"] is True:
            nqueued += 1
        if namekey in finishedJobs:
            nfinished += 1
        if namekey in failedJobs:
            nfailed += 1

    if nfailed > 0:
        print "--- Failed Jobs ----"
        for job in failedJobs:
            print ".",job
    print "----- Job Info -----"
    print "Jobs running: {0}".format(nrunning)
    print "Jobs queued: {0}".format(nqueued)
    print "Jobs finished {0}".format(nfinished)
    print "Jobs failed: {0}".format(nfailed)
    print "--------------------"

    

def main(json, askbeforeResubmitting, JobstoResubmit):
    scripts = ScriptHandling.initScirptListfromJSON(json)
    if JobstoResubmit is None:
        checks = checkJobs(scripts)

        finishedjobs = findfinishedJobs(checks)

        jobs, jobnames = findFailedJobs(scripts, finishedjobs, checks)

        showJobInfo(scripts, checks, finishedjobs, jobnames)

        if len(jobs) >= 1:
            if raw_input("Start resubmission? [y/n] ") == "y":
                resubmit(scripts, jobs, askbeforeResubmitting)

                scripts.saveList("", json)

    else:
        jobs = []
        print "--------------------------"
        print "This script will resubmit:"
        for job in JobstoResubmit:
            jobs.append(("Argument", job))
            print job
        print "--------------------------"
        if raw_input("Start resubmission? [y/n] ") == "y":
            resubmit(scripts, jobs, False)

if __name__ == "__main__":
    import argparse

    argumentparser = argparse.ArgumentParser(
        description='Checking and resubmitting jobs created with ScriptHandling.py'
    )

    argumentparser.add_argument(
        "--json",
        action = "store",
        help = "JSON file, created with ScriptHandling.py containing job info",
        type=str,
        required = True,
    )

    argumentparser.add_argument(
        "--batchResubmit",
        action = "store_false",
        help = "Call without argument! If called all failed jobs will be automatically resubmitted",
    )

    argumentparser.add_argument(
        "--submitJobs",
        nargs='+',
        help = "List of Jobnames to be resumbitted",
        default = None
    )




    arguments = argumentparser.parse_args()

    main(arguments.json, arguments.batchResubmit, arguments.submitJobs)
