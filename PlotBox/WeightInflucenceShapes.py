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
ttbar = False
QCD = True

logging.info("==============================================================================")

if ttbar:
    Files = [
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),88.34,64463096.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),377.96,128391056.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),365.46,108415752.0)
]
if QCD:
    Files = [
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8.root"), 323400 ,58106788.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8.root"),30010,53111380.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.root"),6361,47029440.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.root"),1094,15660391.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.root"),99.31,11107178.0),
        (ROOT.TFile.Open("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/projectSkim/v2/v2/noHLTSel/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.root"),20.20,5331434.0),
    ]
selection = "HLT_ttH_FH == 1 && is_fh == 1 && ht30>500 && jets_pt[5]>40 && nBCSVM>=2"
histos = [("numJets", 5, 5.5 ,10.5), ("ht30",20,500,2500), ("nBCSVM", 3, 1.5, 4.5), ("jets_pt[0]", 65, 50, 800), ("jets_pt[5]", 20, 40, 160)]
xTitles = ["Number of Jets","HT [GeV]", "Number of medium CSV b-tags", "Leading jet p_{T} [GeV]","Sixth jet p_{T} [GeV]"]
if ttbar:
    legendLabels = ["t#bar{t}", "Reweighted t#bar{t}"]
if QCD:
    legendLabels = ["QCD", "Reweighted QCD"]


logging.info("Start making nominal plots")
distrNominal = makeDistribution("Nominal", histos, Files, selection, "1", ROOT.kBlue)

logging.info("Start making reweighted plots")
distrReweighted = makeDistribution("Weighed", histos, Files, selection, "puWeight * (sign(genWeight)) * btagWeight_shape", ROOT.kRed)

finalOutput = []
for iHisto in range(len(distrNominal)):
    logging.info("Making Canvas %s/%s",iHisto+1, len(distrNominal))
    output = RatioPlot(name = str(iHisto))
    output.ratioText = "#frac{Reweighted}{Nominal}"
    output.passHistos([distrNominal[iHisto], distrReweighted[iHisto]], True)
    finalOutput.append(output.drawPlot(legendLabels, xTitles[iHisto]))
if ttbar:
    saveCanvasListAsPDF(finalOutput, "CompShapeWeights_ttbar", ".")
if QCD:
    saveCanvasListAsPDF(finalOutput, "CompShapeWeights_QCD", ".")
