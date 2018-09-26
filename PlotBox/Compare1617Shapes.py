import ROOT
import copy
from ratios import RatioPlot
from PlotHelpers import moveOverUnderFlow, saveCanvasListAsPDF, makeDistribution
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

formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
#############################################################
#############################################################

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

logging.info("==============================================================================")
ttbar = True
QCD = False
if ttbar:
    Files2017 = [
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),88.34,64463096.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),377.96,128391056.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),365.46,108415752.0)]
    Files2016 = [
        (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"),831.76, 76972929)
    ]
if QCD:
    Files2017 = [
        # (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8.root"), 323400 ,58106788.0),
        # (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8.root"),30010,53111380.0),
        # (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.root"),6361,47029440.0),
        # (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.root"),1094,15660391.0),
        # (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.root"),99.31,11107178.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.root"),20.20,5331434.0),
    ]
    Files2016 = [
        # (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 351300 ,54500812.0),
        # (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 31630 ,62178097.0),
        # (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 6802 ,45018815.0),
        # (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 1206 ,15112403.0),
        # (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 120.4 ,3970702.0),
        (ROOT.TFile.Open("/scratch/dsalerno/tth/80x_M17/V25_lepVetoLoose_systematics_v1/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"), 25.25 ,1979791.0),


    ]



selection2017 = "is_fh == 1 && ht30>500 && jets_pt[5]>40 && nBCSVM>=2"
selection2016 = "is_fh == 1 &&   ht>500 && jets_pt[5]>40 && nBCSVM>=2"

mcWeight2017 = "1"
mcWeight2016 = "1"

histos2017 = [("numJets", 5, 5.5 ,10.5), ("ht30",20,500,2500), ("nBCSVM", 3, 1.5, 4.5), ("jets_pt[0]", 65, 50, 800), ("jets_pt[5]", 20, 40, 160), ("HLT_ttH_FH", 2,0,2)]
histos2016 = [("numJets", 5, 5.5 ,10.5), ("ht",20,500,2500), ("nBCSVM", 3, 1.5, 4.5), ("jets_pt[0]", 65, 50, 800), ("jets_pt[5]", 20, 40, 160), ("HLT_ttH_FH", 2,0,2)]
xTitles = ["Number of Jets","HT [GeV]", "Number of medium CSV b-tags", "Leading jet p_{T} [GeV]","Sixth jet p_{T} [GeV]", "HLT comination flag"]

if ttbar:
    legendLabels = ["2017 t#bar{t}", "2016 t#bar{t}"]
if QCD:
    legendLabels = ["2017 QCD2000", "2016 QCD2000"]

assert len(histos2017) == len(histos2016)
assert len(histos2017) == len(xTitles)

logging.info("Start making 2016 plots")
distr2016 = makeDistribution("Plot2016", histos2016, Files2016, selection2016, mcWeight2016, ROOT.kBlue)

logging.info("Start making 2017 plots")
distr2017 = makeDistribution("2017", histos2017, Files2017, selection2017, mcWeight2017, ROOT.kRed)

finalOutput = []
for iHisto in range(len(distr2017)):
    logging.info("Making Canvas %s/%s",iHisto+1, len(distr2017))
    output = RatioPlot(name = str(iHisto))
    output.ratioText = "#frac{2016}{2017}"
    output.passHistos([distr2017[iHisto], distr2016[iHisto]], True)
    finalOutput.append(output.drawPlot(legendLabels, xTitles[iHisto]))
if ttbar:
    saveCanvasListAsPDF(finalOutput, "Comp1617_ttbar", ".")
if QCD:
    saveCanvasListAsPDF(finalOutput, "Comp1617_QCD2000", ".")
