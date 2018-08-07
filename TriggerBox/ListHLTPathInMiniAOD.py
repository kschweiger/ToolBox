import ROOT
from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

def checkTriggerIndex(name,index, names):
    if not 'firstTriggerError' in globals():
        global firstTriggerError
        firstTriggerError = True
    if index>=names.size():
        if firstTriggerError:
            for tr in names: print tr
            print
            print name," not found!"
            print
            firstTriggerError = False
            return False
        else:
            return False
    else:
        return True

def listHLTPaths(filename, triggerLabel, namefilter = ""):
    events = Events([filename])
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), (triggerResults)
    for event in events: break
    event.getByLabel(triggerBitLabel, triggerBits)
    names = event.object().triggerNames(triggerBits.product())
    triggerNames = names.triggerNames()
    for name in triggerNames:
        if name.startswith("HLT") and namefilter in name:
            print name
    
if __name__ == "__main__":
    triggerResults = "TriggerResults::HLT"
    miniAODFile = "/mnt/t3nfs01/data01/shome/koschwei/scratch/testVBFHLT.root"
    listHLTPaths(miniAODFile, triggerResults, "VBF")
