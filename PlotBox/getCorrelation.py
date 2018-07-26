import ROOT
import itertools
import logging
from copy import deepcopy
from plotTools import moveOverUnderFlow2D
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

log_format = (
    '[%(asctime)s] %(levelname)-8s %(funcName)-20s %(message)s')
logging.basicConfig(
    format=log_format,
    level=logging.INFO,
)

def makeHisto(tree, sel, xVar, xBinning, yVar, yBinning):
    name = "{1}:{0}".format(xVar, yVar)
    h2 = ROOT.TH2F(name,name, xBinning[0], xBinning[1], xBinning[2], yBinning[0], yBinning[1], yBinning[2])
    h2.SetTitle("")
    h2.GetXaxis().SetTitle(xVar)
    h2.GetYaxis().SetTitle(yVar)
    tree.Project(name, name, sel)
    moveOverUnderFlow2D(h2, moveUnderFlow = False)
    return h2
    
def getCorrelation(infile, varbin, outfile, selection, treeName = "tree"):
    logging.info("Starting script")
    rFile = ROOT.TFile(infile, "READ")
    tree = rFile.Get(treeName)


    histos = {}
    variables = varbin.keys()
    for xVar, yVar in list(itertools.combinations(variables, 2)):
        logging.info("Getting histo for variable comb %s:%s",xVar, yVar)
        histos["{1}:{0}".format(xVar, yVar)] = makeHisto(tree, selection, xVar, varbin[xVar], yVar, varbin[yVar])
        
    hCorr = ROOT.TH2F("hCorr", "hCorr", len(variables), 0, len(variables), len(variables), 0, len(variables))
    hCorr.SetTitle("CorrelationFactor")
    for b in range(len(variables)):
        hCorr.GetXaxis().SetBinLabel(b+1, variables[b])
        hCorr.GetYaxis().SetBinLabel(b+1, variables[b])
    logging.info("Filling correlation histo")
    for b in range(1, len(variables)+1):
        hCorr.SetBinContent(b,b,1)
    for key in histos:
        yVar, xVar = key.split(":")
        corr = histos[key].GetCorrelationFactor()
        logging.info("Correlation of %s and %s: %s",yVar, xVar, corr)
        hCorr.SetBinContent(variables.index(yVar)+1,variables.index(xVar)+1, corr)
        hCorr.SetBinContent(variables.index(xVar)+1,variables.index(yVar)+1, corr)

    c2Print = []
    logging.info("Make canvas with correltation")
    c = ROOT.TCanvas("c", "c", 1280, 1000)
    c.SetLeftMargin(0.115)
    c.SetRightMargin(0.16)
    c.cd()
    hCorr.Draw("colztext")
    c.Update()
    c2Print.append(c)
    logging.info("Making canvases for 2D histos")
    for key in histos:
        c = ROOT.TCanvas("c"+key, "c"+key, 1280, 1000)
        c.SetLeftMargin(0.115)
        c.SetRightMargin(0.16)
        c.cd()
        histos[key].Draw("colz")
        t = ROOT.TLatex();
        t.SetNDC();
        t.SetTextAlign(22);
        t.SetTextFont(42);
        t.SetTextSizePixels(28);
        t.DrawLatex(0.27,0.92,"Correlation: {0:06.4f}".format(histos[key].GetCorrelationFactor()));
        c.Update()
        c2Print.append(c)

    for icanvas, canvas in enumerate(c2Print):
        if icanvas == 0:
            canvas.Print(outfile+".pdf(")
        elif icanvas == len(c2Print)-1:
            canvas.Print(outfile+".pdf)")
        else:
            canvas.Print(outfile+".pdf")
        
if __name__ == "__main__":
    inp = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root.backup"
    varsAndbinning = { "jets_pt[3]" : (20,40,300),
                       "jets_pt[5]" : (15,40,250),
                       "nBCSVM" : (5,1.5,6.5),
                       "ht30" : (20,500,2500),
    }
    #outfile = "correlation_ttSL_TriggerSel"
    #selection = "is_sl && abs(leps_pdgId[0]) == 13 && (HLT_BIT_HLT_IsoMu27)&&(ht30>500 && jets_pt[5]>40 && nBCSVM>=2) && (HLT_ttH_FH)"
    outfile = "correlation_ttSL_BaseSel"
    selection = "is_sl && abs(leps_pdgId[0]) == 13 && (HLT_BIT_HLT_IsoMu27)&&(ht30>500 && jets_pt[5]>40 && nBCSVM>=2)"

    
    getCorrelation(inp, varsAndbinning, outfile, selection)
