import BatchUtils

class Sciptlist:
    def __init__(self, cmsswpath, basepath, batchtype, scriptpath = "scripts/", logpath = "logs/", errorpath = "logs/", outputpath = "output/"):
        self.scripts = []
        self.scriptsDict = {}
        self.scriptnames = []

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

        self.successKeys = []
        self.failKeys = []

    def addScript(self, jobname , executionstring, outputname, fromJSON = False ):
        thisScript = Script(self.cmsswpath, jobname, self.paths, executionstring, outputname, fromJSON)
        self.scripts.append(thisScript)
        self.scriptsDict[jobname] = thisScript
        self.scriptnames.append(jobname)

    def addSuccessKey(self, key):
        self.successKeys.append(key)

    def addFailKey(self, key):
        self.failKeys.append(key)

    def submission(self):
        for script in self.scripts:
            script.submit(self.system)

    def saveList(self, savePrefix, fullName = None):
        import json
        import time
        lt = time.localtime()

        if fullName is None:
            filename = "{0}_{1}{2:02d}{3:02d}-{4:02d}{5:02d}{6:02d}.json".format(savePrefix, lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)
        else:
            filename = fullName

        dictForJSON = {"General" : { "basepath" : self.basepath ,
                                     "batchsystem" : self.system,
                                     "paths" : self.paths,
                                     "successKeys" : self.successKeys,
                                     "failedKeys" : self.failKeys,
                                     "cmssw" : self.cmsswpath }
                      }
        for script in self.scripts:
            dictForJSON[script.name] = script.getDict()

        with open(filename, 'w') as f:
            f.write(json.dumps(dictForJSON, indent=4))

    def getScriptsByName(self, name):
        if name in self.scriptnames:
            return self.scriptsDict[name]
class Script:
    def __init__(self, cmssw, name, paths, execstring, output, fromJSON, isSubmitted = False):
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
        self.scriptname = "{0}.sh".format(name)
        self.outfilename = output

        self.creationtime = "{0}{1}{2:02d}{3:02d}-{4:02d}{5:02d}{6:02d}".format("",lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)

        self.batchID = None

        self.isSubmitted = isSubmitted

        self.executionstring = execstring
        if not fromJSON:
            BatchUtils.create_script(self.scriptname, self.cmsswpath, self.scriptpath, self.executionstring)


    def getDict(self):
        retdict = {"CreationTime" : self.creationtime,
                   "logfile" : self.logpath+"/"+self.logfilename,
                   "errfile" : self.errpath+"/"+self.errfilename,
                   "outfile" : self.outpath+"/"+self.outfilename,
                   "scriptfile" : self.scriptpath+"/"+self.scriptname,
                   "batchID" : self.batchID,
                   "submitted" : self.isSubmitted,
                   "execstring" : self.executionstring}
        return retdict

    def printScriptInfo(self):
        print "Printing information for script:",self.name
        print "CreationTime",self.creationtime
        print "logfile", self.logpath+"/"+self.logfilename
        print "errfile", self.errpath+"/"+self.errfilename
        print "outfile", self.outpath+"/"+self.outfilename
        print "scriptfile", self.scriptpath+"/"+self.scriptname
        print "batchID", self.batchID
        #print "execstring", self.executionstring

    def submit(self, batchsystem):
        import os
        print self.scriptpath+"/"+self.scriptname
        if os.path.isfile(self.scriptpath+"/"+self.scriptname):
            import subprocess
            if batchsystem == "q":
                output = subprocess.check_output("qsub -l h_vmem=4g -o {0}/{1} -e {2}/{3} {4}/{5}".format(self.logpath, self.logfilename,
                                                                                                          self.errpath, self.errfilename,
                                                                                                          self.scriptpath, self.scriptname),
                                                 shell=True)
                self.batchID = output.split(" ")[2]
                self.isSubmitted = True
        else:
            print "Script not yet created"



def initScirptListfromJSON(jsonfile):
    import json

    with open(jsonfile, 'r') as f:
        readJSON = json.load(f)

    #print readJSON

    scripts = Sciptlist(readJSON["General"]["cmssw"], readJSON["General"]["basepath"], readJSON["General"]["batchsystem"])

    for key in readJSON["General"]["successKeys"]:
        scripts.addSuccessKey(key)
    for key in readJSON["General"]["failedKeys"]:
        scripts.addFailKey(key)


    for key in readJSON:
        if key != "General":
            #print readJSON[key]["outfile"]
            scripts.addScript(key, readJSON[key]["execstring"], readJSON[key]["outfile"].split("/")[-1], True)
            scripts.getScriptsByName(key).isSubmitted = readJSON[key]["submitted"]
            scripts.getScriptsByName(key).batchID = readJSON[key]["batchID"]

    return scripts
