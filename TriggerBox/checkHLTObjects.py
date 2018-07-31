import ROOT
from DataFormats.FWLite import Events, Handle

#############################################################
############### Configure Logging
import logging
log_format = (
    '[%(asctime)s] %(levelname)-8s %(funcName)-20s %(message)s')
logging.basicConfig(
    filename='debug.log',
    format=log_format,
    level=logging.DEBUG,
)

formatter = logging.Formatter(log_format)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
#############################################################
#############################################################


def checkTriggerIndex(name,index, names):
    if index>=names.size():
        for tr in names:
            print tr
        print
        print name," not found!"
        print


def getHLTinfo(filename, eventnumbers, hltnames, controlnames, filters, collections):
    rFile = ROOT.TFile(filename, "READ")
    events = Events(rFile)
    logging.info("getting handle and label")
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults::HLT")
    triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
    patJets, patJetLabel = Handle("vector<pat::Jet>"), ("slimmedJets")
    triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"

    logging.info("Starting Event loop")
    nEvtsFound = 0
    printedOnce = False
    for iev, event in enumerate(events):
        tNames = []
        tcNames = []
        if nEvtsFound == len(eventnumbers):
            break
        if event.eventAuxiliary().event() in eventnumbers:

            nEvtsFound += 1
            logging.info("Precessing event %s",event.eventAuxiliary().event()) 
            event.getByLabel(triggerBitLabel, triggerBits)
            event.getByLabel(triggerObjectLabel, triggerObjects)
            event.getByLabel(triggerPrescaleLabel, triggerPrescales)
            event.getByLabel(patJetLabel, patJets)
            names = event.object().triggerNames(triggerBits.product())
            for iJet, patjet in enumerate(patJets.product()):
                logging.info("Jet %s has csv %s",iJet, max(0.,patjet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")))
            for name in hltnames+controlnames:
                logging.info("Finding version number of numerator and denominator in current run")
                logging.info("Name: %s",name)
                logging.debug(names.triggerNames())
                numset = False
                denomset = False
                for n in names.triggerNames():
                    if n.startswith(name):
                        if name in hltnames:
                            tNames.append(n)
                        else:
                            tcNames.append(n)
                        logging.info("trigger name is now: %s",n)
            for i,tName in enumerate(tNames):
                index = names.triggerIndex(tName)
                checkTriggerIndex(tName,index,names.triggerNames())
                index = names.triggerIndex(tName)
                logging.info("%s accept: %s",tName,triggerBits.product().accept(index))                
                for controlpath in tcNames:
                    indexC = names.triggerIndex(controlpath)
                    logging.info("%s accept: %s",controlpath,triggerBits.product().accept(indexC))
                for j,to in enumerate(triggerObjects.product()):
                    to.unpackNamesAndLabels(event.object(),triggerBits.product())
                    printthisObject = False
                    stuff = []
                    _pt = to.pt()
                    _eta = to.eta()
                    _type = -120
                    for filter_ in to.filterLabels():
                        logging.debug("filter: %s",filter_)
                        if filter_ in filters:
                            printthisObject = True
                            stuff.append(filter_)
                            for t in to.triggerObjectTypes():
                                if t > _type:
                                    _type = t
                    collection_ = to.collection().split("\n")
                    for c in collection_:
                        logging.debug("Found collection %s",c)
                        foundamatchingCollection = False
                        for coll in collections:
                            if c.startswith(coll):
                                foundamatchingCollection = True
                        if foundamatchingCollection:
                            printthisObject = True
                            stuff.append(c)
                            _pt = to.pt()
                            _eta = to.eta()
                            _type = -120
                            for t in to.triggerObjectTypes():
                                if t > _type:
                                    _type = t
                    if printthisObject:
                        logging.info("Object has: %s", stuff)
                        logging.info("    pt %s, eta %s, type %s", _pt, _eta, _type)
                if len(eventnumbers) > 1 and nEvtsFound != len(eventnumbers):
                    raw_input("Next Event")
                    

                    
if __name__ == "__main__":
    _file = "/mnt/t3nfs01/data01/shome/koschwei/scratch/SingleMu_RunE_304125_1696095226_1317.root"
    evtNumbers = [1696095226]
    #evtNumbers = [1679124665]
    HLTNames = ["HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5"]
    ControlNames = ["HLT_IsoMu27"]
    filters = ["hltPFJetForBtagSelector","hltBTagPFCSVp080Single","hltL1sHTT280to500erIorHTT250to340erQuadJet","hltPFJetFilterSixC40","hltPFSixJet40HT430","hltCaloJetFilterSixC35","hltCaloSixJet35HT300"]
    HLTCollections = ["hltPFJetForBtag","hltAK4PFJetsCorrected"]
    getHLTinfo(_file, evtNumbers, HLTNames, ControlNames, filters, HLTCollections)
