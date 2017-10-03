import BatchUtils

class Sciptlist:
    def __init__(self, cmsswpath, basepath, batchtype, scriptpath = "scripts/", logpath = "logs/", errorpath = "logs/", outputpath = "output/"):
        self.scripts = []
        self.basepath = basepath
        self.system = batchtype

        self.scriptpath = scriptpath
        self.logpath = logpath
        self.errorpath = errorpath
        self.outputpath = outputpath

        self.cmsswpath = cmsswpath

        self.paths = { "base" : self.basepath,
                       "scripts" : self.scriptpath,
                       "log" : self.logpath,
                       "err" : self.errorpath,
                       "output" : self.outputpath }

    def addScript(self, jobname , executionstring, outputname ):
        self.scripts.append(Script(self.cmsswpath, jobname, self.paths, executionstring, outputname))

    def submission(self):
        for script in self.scripts:
            script.submit(self.system)

    def saveList(self, savePrefix):
        import json
        import time
        lt = time.localtime()

        filename = "{0}_{1}{2:02d}{3:02d}-{4:02d}{5:02d}{6:02d}.txt".format(savePrefix, lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)

        dictForJSON = {"General" : { "basepath" : self.basepath ,
                                     "batchsystem" : self.system,
                                     "cmssw" : self.cmsswpath }
                      }
        for script in self.scripts:
            dictForJSON[script.name] = script.getDict()

        with open(filename, 'w') as f:
            f.write(json.dumps(dictForJSON, indent=4))
class Script:
    def __init__(self, cmssw, name, paths, execstring, output):
        import time
        lt = time.localtime()

        self.name = name

        self.cmsswpath = cmssw

        self.base = paths["base"]

        self.errpath = "{0}/{1}".format(paths["base"], paths["err"])
        self.logpath = "{0}/{1}".format(paths["base"], paths["log"])
        self.outpath = "{0}/{1}".format(paths["base"], paths["output"])
        self.scriptpath = "{0}/{1}".format(paths["base"], paths["scripts"])

        self.errfilename = "joberr_{0}".format(name)
        self.logfilename = "joblog_{0}".format(name)
        self.scriptpath = "script_{0}".format(name)
        self.outfilename = output

        self.creationtime = "{0}{1}{2:02d}{3:02d}-{4:02d}{5:02d}{6:02d}".format("",lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)

        self.batchID = None

        self.isSubmitted = False

        self.executionstring = execstring

        BatchUtils.create_script(self.name, self.cmsswpath, self.base, self.executionstring)

    def getDict(self):
        retdict = {"CreationTime" : self.creationtime,
                   "logfile" : self.logpath+"/"+self.logfilename,
                   "errfile" : self.errpath+"/"+self.errfilename,
                   "outfile" : self.outpath+"/"+self.outfilename,
                   "batchID" : self.batchID,
                   "execstring" : self.executionstring}
        return self.name, retdict

    def submit(self, batchsystem):
        if self.scriptcreated:
            import subprocess
            if batchsystem == "q":
                output = subprocess.check_output("qsub -l h_vmem=4g -o {0}/{1} -e {2}/{3} {4}".format(self.logpath, self.logfilename,
                                                                                                      self.errpath, self.errfilename,
                                                                                                      self.scriptpath),
                                                 shell=True)
                self.batchID = output.split(" ")[2]
                self.isSubmitted = True
        else:
            print "Script not yet created"
