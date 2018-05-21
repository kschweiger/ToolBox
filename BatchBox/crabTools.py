import os,sys

def kill(directories, dryrun = False):
    for directory in directories:
        dirs = os.walk(directory)
        subdirs = next(dirs)[1]
        
        if "inputs" in subdirs and "results" in subdirs:
            if dryrun:
                print "crab kill {0}".format(directory)
            else:
                os.system("crab kill {0}".format(directory))
        else:
            for dir_ in subdirs:
                if dryrun:
                    print "crab kill {0}/{1}".format(directory, dir_)
                else:
                    os.system("crab kill {0}/{1}".format(directory, dir_))

    return True
                
def status(directories, dryrun = False):
    for directory in directories:
        print "--------------------------------------------------------------"
        dirs = os.walk(directory)
        subdirs = next(dirs)[1]
        
        if "inputs" in subdirs and "results" in subdirs:
            if dryrun:
                print "crab status {0}".format(directory)
            else:
                os.system("crab status {0}".format(directory))
        else:
            for dir_ in subdirs:
                print "--------------------------------------------------------------"
                if dryrun:
                    print "crab status {0}/{1}".format(directory, dir_)
                else:
                    os.system("crab status {0}/{1}".format(directory, dir_))

    return True                

def resubmit(directories, blacklist = None, whitelist = None, maxmemory = None, walltime = None, dryrun = False):
    for directory in directories:
        if directory.endswith("/"):
            directory = directory[:-1] #remove tailing /
        command = "crab resubmit"
        if blacklist is not None:
            sites = ",".join(blacklist)
            command = "{0} --siteblacklist={1}".format(command, sites)
        if whitelist is not None:
            sites = ",".join(whitelist)
            command = "{0} --sitewhitelist={1}".format(command, sites)
        if maxmemory is not None:
            command = "{0} --maxmemory={1}".format(command, maxmemory)
        if walltime is not None:
            command = "{0} --maxmemory={1}".format(command, walltime*60)

        command_ = command
        dirs = os.walk(directory)
        subdirs = next(dirs)[1]

        if "inputs" in subdirs and "results" in subdirs:
            command = "{0} {1}".format(command_, directory)
            if dryrun:
                print command
            else:
                os.system(command)
        else:
            for dir_ in subdirs:
                command = "{0} {1}/{2}".format(command_, directory, dir_)                
                if dryrun:
                    print command
                else:
                    os.system(command)

    return True


def getJobSummary(directories, brief):
    import subprocess

    
    for directory in directories:
        dirs = os.walk(directory)
        subdirs = next(dirs)[1]
        if "inputs" in subdirs and "results" in subdirs:
            proc = subprocess.Popen("crab status {0}".format(directory),
                                    shell=True,stdout=subprocess.PIPE)
            a = proc.communicate()
            status, taskname, summary = parseJobOut(a[0])
            print "--------------------------------------------------------------------------------------------"
            print "---",taskname
            if summary is not None:
                for name in summary:
                    if brief:
                        print "Average {0}: {1}".format(name,summary[name]["ave"])
                    else:
                        print "Status: {0}".format(status)

    
        else:
            for dir_ in subdirs:
                proc = subprocess.Popen("crab status {0}/{1}".format(directory, dir_),
                                        shell=True,stdout=subprocess.PIPE)
                a = proc.communicate()
                status, taskname, summary = parseJobOut(a[0])
                print "--------------------------------------------------------------------------------------------"
                print "---",taskname
                if summary is not None:
                    for name in summary:
                        if brief:
                            print "Average {0}: {1}".format(name,summary[name]["ave"])
                        else:
                            print summary[name]
                else:
                    print "Status: {0}".format(status)
                        
                    
    return True

def parseJobOut(output):
    lines = output.split("\n")
    taskname = ""
    status = ""
    for line in lines:
        if line.startswith("Task name:"):
            taskname = line.split("\t")[-1]
        if line.startswith("Jobs status:"):
            if "running" in line:
                status = "Running"
            elif "idle" in line:
                status = "Pending"
            elif "finished" in line:
                status = "Finished"
            else:
                status = "Check job output!"
    try:
        sumStart = lines.index("Summary of run jobs:")
    except ValueError:
        return status, taskname, None
    items = lines[sumStart+1:sumStart+5]
    memoryItems = items[0].replace("Memory:",",").split(",")[1:]
    runTimeItems = items[1].replace("Runtime:",",").split(",")[1:]
    cpuEffItems = items[2].replace("CPU eff:",",").split(",")[1:]
    summary = {}
    for name, items in [("Memory", memoryItems),("Runtime", runTimeItems),("CPU", cpuEffItems)]:
        summary[name] = {}
        for item in items:
            res = list(reversed(item.split(" ")[1:]))
            summary[name][res[0]] = res[1]

    return status, taskname, summary
                
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Handling crab jobs')
    parser.add_argument('--dir', action="store", required=True, help="Directory of all jobs", nargs='+', type=str)
    parser.add_argument("--kill", action = "store_true", help="Kill jobs")
    parser.add_argument("--resubmit", action = "store_true", help="resubmit jobs")
    parser.add_argument("--status", action = "store_true", help="job status")
    parser.add_argument("--summary", action = "store_true", help="Parse job summary for memory, runtime, cpuusage")
    parser.add_argument("--brief", action = "store_true", help="Parse job summary for memory, runtime, cpuusageOnly print brief summary")
    parser.add_argument("--dryrun", action = "store_true", help="Instead of executing the command the command is printed")
    parser.add_argument("--blacklist", action = "store", help = "Blacklist for resubmission", nargs='+', type=str, default = None)
    parser.add_argument("--whitelist", action = "store", help = "Blacklist for resubmission", nargs='+', type=str, default = None)
    parser.add_argument("--maxmemory", action = "store", help = "Maximum memory for resubmission (Crab default 2500)", type=str, default = None)
    parser.add_argument("--walltime", action = "store", help = "Maximum wall time for resubmission in hours! HOURS! (Crab default 1315 minutes - 21h 50min)", type=int, default = None)
    args = parser.parse_args()

    if int(args.kill) + int(args.resubmit) + int(args.status) + int(args.summary) > 1:
        print "Either killing or resubmitting"
        exit()
    elif int(args.kill) + int(args.resubmit) + int(args.status)  + int(args.summary)  == 0:
        print "Please set at least on of the arguments"
        print "    --kill | --status | --resubmit"
    

    if args.dryrun:
        print "         +--------------------------------------------------+"
        print "         |                      Dryrun                      |"
        print "         | The commands will be printed instead of executed |"
        print "         +--------------------------------------------------+"
        
    if args.kill:
        ret = kill(args.dir, args.dryrun)

    if args.resubmit:
        ret = resubmit(args.dir, args.blacklist, args.whitelist, args.maxmemory, args.walltime, args.dryrun)

    if args.status:
        ret = status(args.dir, args.dryrun)


    if args.summary:
        ret = getJobSummary(args.dir, args.brief)
    
        

    if ret is True and not args.dryrun:
        wdir = os.getcwd()
        if not os.path.isfile(wdir+"/crabTools.log"):
            os.system("touch "+wdir+"/crabTools.log")

        runcommand = "python "
        for arg in sys.argv:
            runcommand += arg + " "
            
        with open(wdir+"/crabTools.log", "a") as logfile:
            logfile.write(runcommand+"\n")
