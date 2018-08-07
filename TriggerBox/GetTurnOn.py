import ROOT
import time
from copy import deepcopy
from collections import OrderedDict
import os
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
 
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
if True:
    ROOT.gErrorIgnoreLevel = ROOT.kWarning# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
    
def initplot(name, namepostfix, bins, startbin, endbin, title, color):
    histo = ROOT.TH1F(name+"_"+namepostfix, name+"_"+namepostfix, bins, startbin, endbin)
    histo.SetLineColor(color)
    histo.SetTitle("")
    histo.GetXaxis().SetTitle(title)
    return histo

def treeLoop(fileName, hDictDenom, hDictNum, hdictFail = None):
    t0 = time.time()
    rFile = ROOT.TFile.Open(fileName)
    tree = rFile.Get("tree")
    nEvents = tree.GetEntries()
    logging.info("Will loop over %s events", nEvents)
    tdiff = time.time()
    evtsProcessed = 0
    npassingNum = 0
    for iev in range(nEvents):
        tree.GetEvent(iev)
        if iev%100000 == 0 and iev != 0:
            logging.info("Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff))
            tdiff = time.time()
        if iev >= 1000000:
            break
        passBaseline = False
        passTrigger = False
        #if tree.numJets >= 4 and tree.is_fh == 1 and tree.nBCSVM >= 4 and tree.HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40 == 1:
        if tree.numJets >= 6 and tree.is_fh == 1 and tree.nBCSVM >= 1 and tree.HLT_BIT_HLT_PFHT430_SixPFJet40 == 1:
            passBaseline = True
        #if tree.HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 == 1:
        if tree.HLT_BIT_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5== 1:
            passTrigger = True
        if passBaseline:
            nJets = 0
            pts = []
            csvs = []
            for iJet in range(len(tree.jets_pt)):
                if tree.jets_pt[iJet] > 30 and abs(tree.jets_eta[iJet]) < 2.4:
                    nJets += 1
                    pts.append(tree.jets_pt[iJet])
                    csvs.append(tree.jets_btagCSV[iJet])

            csvs = sorted(csvs, reverse = True)

            #hDictDenom["nJets"].Fill(nJets)
            hDictDenom["nbJets"].Fill(tree.nBCSVM)
            #hDictDenom["JetPtLeading"].Fill(pts[0])
            #hDictDenom["JetPt2ndLeading"].Fill(pts[1])
            #hDictDenom["JetPt3rdLeading"].Fill(pts[2])
            #hDictDenom["JetPt4thLeading"].Fill(pts[3])
            hDictDenom["JetCSVLeading"].Fill(csvs[0])
            hDictDenom["JetCSV2ndLeading"].Fill(csvs[1])
            hDictDenom["JetCSV3rdLeading"].Fill(csvs[2])
            hDictDenom["JetCSV4thLeading"].Fill(csvs[3])
            #hDictDenom["HT"].Fill(tree.ht30)
            if passTrigger:
                #hDictNum["nJets"].Fill(nJets)
                hDictNum["nbJets"].Fill(tree.nBCSVM)
                #hDictNum["JetPtLeading"].Fill(pts[0])
                #hDictNum["JetPt2ndLeading"].Fill(pts[1])
                #hDictNum["JetPt3rdLeading"].Fill(pts[2])
                #hDictNum["JetPt4thLeading"].Fill(pts[3])
                hDictNum["JetCSVLeading"].Fill(csvs[0])
                hDictNum["JetCSV2ndLeading"].Fill(csvs[1])
                hDictNum["JetCSV3rdLeading"].Fill(csvs[2])
                hDictNum["JetCSV4thLeading"].Fill(csvs[3])
                #hDictNum["HT"].Fill(tree.ht30)
                npassingNum += 1
            else:
                if hdictFail is not None:
                    #hdictFail["nJets"].Fill(nJets)
                    hdictFail["nbJets"].Fill(tree.nBCSVM)
                    #hdictFail["JetPtLeading"].Fill(pts[0])
                    #hdictFail["JetPt2ndLeading"].Fill(pts[1])
                    #hdictFail["JetPt3rdLeading"].Fill(pts[2])
                    #hdictFail["JetPt4thLeading"].Fill(pts[3])
                    hdictFail["JetCSVLeading"].Fill(csvs[0])
                    hdictFail["JetCSV2ndLeading"].Fill(csvs[1])
                    hdictFail["JetCSV3rdLeading"].Fill(csvs[2])
                    hdictFail["JetCSV4thLeading"].Fill(csvs[3])
                    #hdictFail["HT"].Fill(tree.ht30)
            evtsProcessed += 1
            
    logging.info("Events processed: {0}".format(evtsProcessed))
    logging.info("Events passing numerator: {0}".format(npassingNum))
    logging.info("Total time: {0:8f}".format(time.time()-t0))
    return evtsProcessed   

def saveCanvasListAsPDF(listofCanvases, outputfilename, foldername = "."):
    logging.info("Writing outputfile %s.pdf",outputfilename)
    for icanvas, canves in enumerate(listofCanvases):
        logging.info("Writing canvas [%s/%s]", icanvas, len(listofCanvases)-1)
        if icanvas == 0:
            canves.Print(foldername+"/"+outputfilename+".pdf(")
        elif icanvas == len(listofCanvases)-1:
            canves.Print(foldername+"/"+outputfilename+".pdf)")
        else:
            canves.Print(foldername+"/"+outputfilename+".pdf")

def saveHistosAsROOT(histosList, outfileName, foldername):
    logging.info("Writing outputfile %s.root",outfileName)
    out = ROOT.TFile(foldername+"/"+outfileName+".root", "RECREATE")
    out.cd()
    for obj in histosList:
        for plottype in obj.keys():
            for plot in obj[plottype].keys():
                obj[plottype][plot].Write()
    out.Close()



def getTurnOn(data, mc, outfilename ,foldername):
    plots = OrderedDict()
    #plots.update({"nJets" : ("hnJets", 20,-0.5,19.5, "Number of Jets")})
    plots.update({"nbJets" : ("hnbJets", 20,-0.5,19.5, "Number of b-tagged Jets")})
    #plots.update({"HT" : ("hht", 24,300,1500, "HT")})
    #plots.update({"JetPtLeading" : ("hJetPtLeading", 80, 50, 750, "Leading jet p_{T}")})
    #plots.update({"JetPt2ndLeading" : ("hJetPt2ndLeading", 30, 50, 550, "2nd leading jet p_{T}")})
    #plots.update({"JetPt3rdLeading" : ("hJetPt3rdLeading", 30, 50, 550, "3rd leading jet p_{T}")})
    #plots.update({"JetPt4thLeading" : ("hJetPt4thLeading", 20 , 30, 300, "4th leading jet p_{T}")})
    plots.update({"JetCSVLeading" : ("hJetcsvLeading",20,0,1, "CSV of Jet with highest CSV")})
    plots.update({"JetCSV2ndLeading" : ("hJetcsv2ndLeading",20,0,1, "CSV of Jet with 2nd highest CSV")})
    plots.update({"JetCSV3rdLeading" : ("hJetcsv3rdLeading",20,0,1, "CSV of Jet with 3rd highest CSV")})
    plots.update({"JetCSV4thLeading" : ("hJetcsv4thLeading",20,0,1, "CSV of Jet with 4th highest CSV")})

    logging.info("Making plot dicts")
    histosDataDenom = {}
    histosMCDenom = {}
    histosDataNum = {}
    histosMCNum = {}
    histosDataFail = {}
    histosMCFail = {}
    titles = {}
    for plot in plots:
        hname, nBins, firstBin, lastBin, xTitle = plots[plot]
        histosDataDenom[plot] = initplot(hname, "DataDenom", nBins, firstBin, lastBin, xTitle, ROOT.kBlue)
        histosMCDenom[plot] = initplot(hname, "MCDenom", nBins, firstBin, lastBin, xTitle, ROOT.kRed)
        histosDataNum[plot] = initplot(hname, "DataNum", nBins, firstBin, lastBin, xTitle, ROOT.kBlue)
        histosMCNum[plot] = initplot(hname, "MCNum", nBins, firstBin, lastBin, xTitle, ROOT.kRed)
        histosDataFail[plot] = initplot(hname, "DataFail", nBins, firstBin, lastBin, xTitle, ROOT.kBlue)
        histosMCFail[plot] = initplot(hname, "MCFail", nBins, firstBin, lastBin, xTitle, ROOT.kRed)
        titles[plot] = xTitle
    logging.info("Starting data loop")
    treeLoop(data, histosDataDenom, histosDataNum, histosDataFail)
    logging.info("Starting mc loop")
    treeLoop(mc, histosMCDenom, histosMCNum, histosMCFail)

    denoms = [histosDataDenom,histosMCDenom]
    nums = [histosDataNum,histosMCNum]
    fails = [histosDataFail, histosMCFail]
    allCanvas = []

    leg = ROOT.TLegend(0.4,0.4,0.7,0.6)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.05)
    onekey = denoms[0].keys()[0]
    leg.AddEntry(denoms[0][onekey], "data", "PLE")
    leg.AddEntry(denoms[1][onekey], "t#bar{t} AH", "PLE")
    
    if not os.path.exists(foldername):
        logging.warning("Creating folder: {0}".format(foldername))
        os.makedirs(foldername)

    
    for iplot, plot in enumerate(plots):
        logging.info("Plotting %s",plot)
        canvas = ROOT.TCanvas("c"+str(plot)+str("denom"), "c"+str(plot)+str("denom"), 5, 30, 640, 580)

        """
        canvas.SetTopMargin(0.08*.75)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.11)
        canvas.SetBottomMargin(0.12)
        """
        canvas.cd()
        denoms[0][plot].GetYaxis().SetTitle("Denominator Events")
        denoms[0][plot].DrawNormalized("histoe")
        denoms[1][plot].DrawNormalized("histoesame")
        leg.Draw("same")
        canvas.Update()
        allCanvas.append(deepcopy(canvas))

        canvas1 = ROOT.TCanvas("c"+str(plot)+str("num"), "c"+str(plot)+str("num"), 5, 30, 640, 580)

        """
        canvas.SetTopMargin(0.08*.75)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.11)
        canvas.SetBottomMargin(0.12)
        """
        canvas1.cd()
        nums[0][plot].GetYaxis().SetTitle("Numerator Events")
        nums[0][plot].DrawNormalized("histoe")
        nums[1][plot].DrawNormalized("histoesame")
        leg.Draw("same")
        canvas1.Update()
        allCanvas.append(deepcopy(canvas1))

        
        canvas1p1 = ROOT.TCanvas("c"+str(plot)+str("fail"), "c"+str(plot)+str("num"), 5, 30, 640, 580)

        """
        canvas.SetTopMargin(0.08*.75)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.11)
        canvas.SetBottomMargin(0.12)
        """
        canvas1p1.cd()
        fails[0][plot].GetYaxis().SetTitle("Failed Events")
        fails[0][plot].DrawNormalized("histoe")
        fails[1][plot].DrawNormalized("histoesame")
        leg.Draw("same")
        canvas1p1.Update()
        allCanvas.append(deepcopy(canvas1p1))

        
        
        canvas2 = ROOT.TCanvas("c"+str(plot)+str("Eff"), "c"+str(plot)+str("Eff"), 5, 30, 640, 580)

        """
        canvas.SetTopMargin(0.08*.75)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.11)
        canvas.SetBottomMargin(0.12)
        """
        canvas2.cd()

        
        grData = ROOT.TGraphAsymmErrors(histosDataNum[plot], histosDataDenom[plot])
        grMC = ROOT.TGraphAsymmErrors(histosMCNum[plot], histosMCDenom[plot])

        
        grData.GetXaxis().SetTitle(titles[plot])
        grData.GetYaxis().SetTitleSize(0.069*0.75)
        grData.GetYaxis().SetTitleOffset(1.05)
        grData.GetYaxis().SetLabelSize(0.060*0.75)
        grData.GetXaxis().SetTitleSize(0.069*0.75)
        grData.GetXaxis().SetLabelSize(0.06*0.75)
        grData.GetXaxis().SetDecimals(1)
        grData.GetYaxis().SetDecimals(1)
        grData.GetXaxis().SetNdivisions(20504)
        grData.GetYaxis().SetNdivisions(505)
        grData.GetYaxis().SetRangeUser(0.0,1.1)
        
        grMC.SetTitle()
        grMC.GetYaxis().SetTitleSize(0.069*0.75)
        grMC.GetYaxis().SetTitleOffset(1.05)
        grMC.GetYaxis().SetLabelSize(0.060*0.75)
        grMC.GetXaxis().SetTitleSize(0.069*0.75)
        grMC.GetXaxis().SetLabelSize(0.06*0.75)
        grMC.GetXaxis().SetDecimals(1)
        grMC.GetYaxis().SetDecimals(1)
        grMC.GetXaxis().SetNdivisions(20504)
        grMC.GetYaxis().SetNdivisions(505)
        grMC.GetYaxis().SetRangeUser(0.0,1.1)
        
        grData.Draw("AP")
        grMC.Draw("PSame")
        leg.Draw("same")
        canvas2.Update()
        allCanvas.append(deepcopy(canvas2))
        
    saveCanvasListAsPDF(allCanvas, outfilename, foldername)
            

        
if __name__ == "__main__":
    """
    data = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_passAll_v1/QuadJetControl/BTagCSV.root"
    mc = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_passAll_v1/QuadJetControl/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root"
    """
    data = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_passAll_v1/SixJetControl/JetHT.root"
    mc = "/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_passAll_v1/SixJetControl/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root"
    
    baseSel = "1"
    triggerSel = "(HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07 || HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)"

    getTurnOn(data, mc, "6j1t_turnon", "turnOns")
