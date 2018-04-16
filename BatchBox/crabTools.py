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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Handling crab jobs')
    parser.add_argument('--dir', action="store", required=True, help="Directory of all jobs", nargs='+', type=str)
    parser.add_argument("--kill", action = "store_true", help="Kill jobs")
    parser.add_argument("--resubmit", action = "store_true", help="resubmit jobs")
    parser.add_argument("--status", action = "store_true", help="job status")
    parser.add_argument("--dryrun", action = "store_true", help="Instead of executing the command the command is printed")
    parser.add_argument("--blacklist", action = "store", help = "Blacklist for resubmission", nargs='+', type=str, default = None)
    parser.add_argument("--whitelist", action = "store", help = "Blacklist for resubmission", nargs='+', type=str, default = None)
    parser.add_argument("--maxmemory", action = "store", help = "Maximum memory for resubmission (Crab default 2500)", type=str, default = None)
    parser.add_argument("--walltime", action = "store", help = "Maximum wall time for resubmission in hours! HOURS! (Crab default 1315 minutes - 21h 50min)", type=int, default = None)
    args = parser.parse_args()

    if args.kill and args.resubmit:
        print "Either killing or resubmitting"
        exit()

    if args.dryrun:
        print "         +--------------------------------------------------+"
        print "         |                      Dryrun                      |"
        print "         | The commands will be printed instead of executed |"
        print "         +--------------------------------------------------+"
        
    if args.kill:
        kill(args.dir, args.dryrun)

    if args.resubmit:
        resubmit(args.dir, args.blacklist, args.whitelist, args.maxmemory, args.walltime, args.dryrun)

    if args.status:
        status(args.dir, args.dryrun)
