import ROOT
from DataFormats.FWLite import Events, Handle

#############################################################
############### Configure Logging
import logging
log_format = (
    '%(levelname)-8s %(message)s')
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
def getInfo(filename, eventnumbers):
    rFile = ROOT.TFile(filename, "READ")
    events = Events(rFile)
    logging.info("getting handle and label")
    patJets, patJetLabel = Handle("vector<pat::Jet>"), ("slimmedJets")
    patEle, patElelabel = Handle("vector<pat::Electron>"), ("slimmedElectrons")
    patMu, patMulabel = Handle("vector<pat::Muon>"), ("slimmedMuons")
    nEvtsFound = 0

    logging.info("Starting Event loop")
    for iev, event in enumerate(events):
        if nEvtsFound == len(eventnumbers):
            break
        if event.eventAuxiliary().event() in eventnumbers:
            nEvtsFound += 1
            
            event.getByLabel(patJetLabel, patJets)
            event.getByLabel(patElelabel, patEle)
            event.getByLabel(patMulabel, patMu)

            for iJet, patjet in enumerate(patJets.product()):
                jetEnergyUncorrected = (patjet.chargedHadronEnergy() + patjet.neutralHadronEnergy()+ patjet.photonEnergy()
                                        + patjet.electronEnergy()+ patjet.muonEnergy()+ patjet.HFEMEnergy())
                logging.info("Jet {0}: csv {1:1.2f} | pt {2:03.2f} | eta {3:1.4f} | energy (uncorr) {4:03.2f}".format(
                    iJet,
                    max(0.,patjet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")),
                    patjet.pt(), patjet.eta(),
                    jetEnergyUncorrected)
                )
                logging.info("Jet {0}: NHF {1:01.2f} | NEF {2:01.2f} | NConst {3:2} | CHF {4:01.2f} | CEF {5:01.2f} | Mult {6:2}".format(
                    iJet,
                    patjet.neutralHadronEnergyFraction(),
                    patjet.neutralEmEnergyFraction(),
                    patjet.numberOfDaughters(),
                    patjet.chargedHadronEnergyFraction(),
                    patjet.chargedEmEnergyFraction(),
                    patjet.chargedMultiplicity())
                )
            for iEle, ele in enumerate(patEle.product()):
                logging.info("Electron {0} has pt {1:03.2f} and eta {2:1.4f}".format(iEle, ele.pt(), ele.eta()))

 


        
if __name__ == "__main__":
    _file = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/sync/ttHbb/CC0FCC49-B50A-E811-9694-02163E0144C8.root"
    evtNumbers = [3308882]
    getInfo(filename = _file, eventnumbers = evtNumbers)
