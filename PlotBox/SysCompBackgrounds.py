import ROOT
from copy import deepcopy

#############################################################
# General ROOT config settings
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#############################################################

def setStyle(histo, color, xAxisTitle, yAxisTitle):
    histo.SetLineColor(color)
    histo.SetTitle("")
    histo.GetXaxis().SetTitle(xAxisTitle)
    histo.GetYaxis().SetTitle(yAxisTitle)
    histo.GetYaxis().SetTitleOffset(histo.GetYaxis().GetTitleOffset()* 1.3)
    histo.GetXaxis().SetTitleOffset(histo.GetXaxis().GetTitleOffset()* 1.2)

def getCanvas(name = "c1", ratio = False):
    """
    Function for generation a TCanvas object.

    Parameters:
    -----------
    name : string
        Name of the canvas
    ratio : bool
        If True, the functions returns TCanvas with to pads. Pad 1 for
        the plot and Pad 2 for the ratio
    """

    print "        Creating canvas with name {0}".format(name)

    cwidth = 1600
    cheight = 1280

    canvas = ROOT.TCanvas(name, name, cwidth, cheight)

    margins = [0.06, 0.04, 0.1, 0.1]

    if not ratio:
        canvas.SetTopMargin(margins[0])
        canvas.SetRightMargin(margins[1])
        canvas.SetLeftMargin(margins[2])
        canvas.SetBottomMargin(margins[3])

    else:
        canvas.Divide(1,2)
        canvas.cd(1).SetPad(0.,0.3-0.02,1.0,0.975)
        canvas.cd(2).SetPad(0.,0.0,1.0,0.3*(1-0.02))
        canvas.cd(1).SetBottomMargin(0.02)
        canvas.cd(2).SetTopMargin(0.00)
        canvas.cd(1).SetTopMargin(margins[0])
        canvas.cd(2).SetBottomMargin(margins[3]*(1/0.3))
        canvas.cd(1).SetRightMargin(margins[1])
        canvas.cd(1).SetLeftMargin(margins[2])
        canvas.cd(2).SetRightMargin(margins[1])
        canvas.cd(2).SetLeftMargin(margins[2])
        canvas.cd(2).SetTicks(1,1)
        canvas.cd(1).SetTicks(1,1)
        canvas.cd(2).SetFillStyle(0)
        canvas.cd(1).SetFillStyle(0)
        canvas.cd(2).SetFillColor(0)
        canvas.cd(2).SetFrameFillStyle(4000)

    return canvas

def drawHistos(orderedHistoList, stackindex = None, canvas = None, orderedRatioList = None):
    """
    Function that draws all histograms that are given to it.

    Parameters
    ----------
    orderedHistolist : list, elements: tuples
        list with all histograms in order they have to be drawn. Each element
        is expected to be a tuple of ROOT.TH1 and DrawString
    orderedRatioList : list, elements: tuples
        list with all ratio histos. Each element is expected to be a tuple of
        ROOT.TH1 and DrawString.
    stackindex : int
        if int is given the histogram with the index is expected to be a THStack

    Returns:
    --------
    ROOT.TCanvas
    """
    #Get global maximal bin height
    maxval = 0
    for histo, drawstring in orderedHistoList:
        if histo.GetMaximum() > maxval:
            maxval = histo.GetMaximum()


    if canvas is None:
        if orderedRatioList is None:
            print "        Creaing new canvas"
            thiscanvas = getCanvas()
        else:
            print "        Creaing new canvas with ratio"
            thiscanvas = getCanvas(ratio = True)
    else:
        print "        Using canvas given as parameter"
        thiscanvas = canvas


    if orderedRatioList is not None:
        thiscanvas.cd(2)
        idrawn = 0
        drawpostfix = ""
        for ratio, drawstring in orderedRatioList:
            print "        Drawing {0} with option {1}{2}".format(ratio.GetName(),drawstring, drawpostfix)
            ratio.Draw("{0}{1}".format(drawstring, drawpostfix))
            #ratio.GetYaxis().SetLabelSize(0) #TODO change to Data / MC or something
            if idrawn == 0:
                #drawpostfix = " same"
                pass
            idrawn += 1
    thiscanvas.Update()
    #raw_input("keep drawing")

    thiscanvas.cd(1)
    idrawn = 0
    drawpostfix = ""

    if stackindex is None:
        for histo, drawstring in orderedHistoList:
            print "        Drawing {0} with option {1}{2}".format(histo.GetName(),drawstring, drawpostfix)
            if idrawn == 0:
                histo.GetYaxis().SetRangeUser(0, maxval *  1.1)
            if idrawn == 0 and orderedRatioList is not None:
                histo.GetXaxis().SetLabelSize(0)
                histo.GetYaxis().SetTitleSize(histo.GetYaxis().GetTitleSize() * 1.4)
                histo.GetYaxis().SetTitleOffset(histo.GetYaxis().GetTitleOffset() * (1/1.3))
                histo.GetYaxis().SetLabelSize(histo.GetYaxis().GetLabelSize() * 1.4)
            histo.Draw("{0}{1}".format(drawstring, drawpostfix))
            if idrawn == 0:
                drawpostfix = " same"
            idrawn += 1
    thiscanvas.Update()
    return thiscanvas


def getRatioPlot(hRef, hList):
    """
    Function for generating the histograms used in a ratioplot.

    Parameters
    ----------
    hRef : ROOT.TH1
        This histogram will be used as reference histo (unity line in the plot)
    hList : list, elements: ROOT.TH1
        This list contains all further histograms for the ratio plot

    Returns:
    --------
    hRatioRef : ROOT.TH1F
        Reference line
    hRatioList : list, elements: ROOT.TH1
        List with all further histograms in the ratio plot
    div : tuple (maxdiv, mindiv)
        Tuple containing global maximum and minimum of all
        histos considered for the ratio
    """

    gRef = ROOT.TGraphErrors(hRef)

    line = hRef.Clone()
    line.SetName("ratioline_"+line.GetName())
    line.SetTitle("")
    line.Divide(hRef)
    line.SetLineColor(1)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.SetFillStyle(0)

    line.GetXaxis().SetLabelSize(line.GetXaxis().GetLabelSize()*(1/0.3))
    line.GetYaxis().SetLabelSize(line.GetYaxis().GetLabelSize()*(1/0.3))
    line.GetXaxis().SetTitleSize(line.GetXaxis().GetTitleSize()*(1/0.3))
    line.GetYaxis().SetTitleSize(line.GetYaxis().GetTitleSize()*(1/0.3))
    line.GetYaxis().SetNdivisions(505)
    #line.GetXaxis().SetNdivisions(config.getint("General","xNdiv"))

    for i in range(line.GetNbinsX()+1):
            line.SetBinContent(i,1)
            line.SetBinError(i,0)
    print "        Ratio line generated: "+str(line)

    mindiv = 9999.
    maxdiv = -9999.

    hRatioList = []

    for h in hList:
        ref = ROOT.TGraphAsymmErrors(hRef)
        ref.SetMarkerColor(hRef.GetLineColor())
        ref.SetLineColor(hRef.GetLineColor())
        print "        Making ratio for ratio plot from "+str(h)
        ratio = ref.Clone()
        ratio.SetName("ratio_"+h.GetName())
        ratio.SetMarkerColor(h.GetLineColor())
        ratio.SetLineColor(h.GetLineColor())
        x, y = ROOT.Double(0), ROOT.Double(0)
        for i in range(0,ref.GetN()):
            ref.GetPoint(i, x, y)
            currentBin = h.FindBin(x)
            currentBinContent = h.GetBinContent(currentBin)
            if currentBinContent > 0:
                ratioval = currentBinContent/y
                ratio.SetPoint(i, x, ratioval)
                if ratioval > maxdiv and ratioval > 0:
                    maxdiv = round(ratioval, 1)
                if ratioval < mindiv and ratioval > 0:
                    mindiv = round(ratioval, 1)
            else:
                ratio.SetPoint(i, x, -999)

            if y > 0:
                if currentBinContent > 0:
                    ratio.SetPointEYlow(i, ref.GetErrorYlow(i)/currentBinContent)
                    ratio.SetPointEYhigh(i, ref.GetErrorYhigh(i)/currentBinContent)
                else:
                    ratio.SetPointEYlow(i, 1-(y-ref.GetErrorYlow(i))/y)
                    ratio.SetPointEYhigh(i, (y+ref.GetErrorYhigh(i))/y-1)
            else:
                ratio.SetPointEYlow(i, 0)
                ratio.SetPointEYhigh(i, 0)
        hRatioList.append(deepcopy(ratio))
        del ratio

    #logging.debug("Maximum deviation is: +{0} -{1}".format(maxdiv, mindiv))
    #line.GetYaxis().SetRangeUser(mindiv, maxdiv)

    if maxdiv < 1.1 and mindiv > 0.9:
        line.GetYaxis().SetRangeUser(0.85,1.15)
    elif maxdiv < 1.25 and mindiv > 0.75:
        line.GetYaxis().SetRangeUser(0.7,1.3)
    else:
        line.GetYaxis().SetRangeUser(0.2,1.8)

    hRatioRef = line

    return hRatioRef, hRatioList


def getBackgroundSum(inputRootfile, distribution, bkgList, systematic = None):
    backgroundSum = None

    if systematic is None:
        hNamePostFix = distribution
    else:
        hNamePostFix = "{0}__{1}".format(distribution, systematic)

    for ibkg, bkg in enumerate(bkgList):
        print bkg
        if ibkg == 0:
            backgroundSum = inputRootfile.Get("{0}__{1}".format(bkg, hNamePostFix)).Clone()
            print inputRootfile.Get("{0}__{1}".format(bkg, hNamePostFix)).Clone()
            backgroundSum.SetName("BackgroundSum__{0}".format(hNamePostFix))
        else:
            print inputRootfile.Get("{0}__{1}".format(bkg, hNamePostFix)).Clone()
            backgroundSum.Add(inputRootfile.Get("{0}__{1}".format(bkg, hNamePostFix)))

    return backgroundSum

def makeSystComparison(inputfile, category, backgroundlist, systematic):
    print "Making comparison plot for systematic "+systematic
    rFile = ROOT.TFile().Open(inputfile)

    distributions = {"j7t3":"fh_j7_t3__mem_FH_4w2h1t_p",
                     "j7t4":"fh_j7_t4__mem_FH_3w2h2t_p",
                     "j8t3":"fh_j8_t3__mem_FH_4w2h1t_p",
                     "j8t4":"fh_j8_t4__mem_FH_3w2h2t_p",
                     "j9t3":"fh_j9_t3__mem_FH_4w2h1t_p",
                     "j9t4":"fh_j9_t4__mem_FH_4w2h2t_p"}

    variable = distributions[category]

    print "    Getting background sums"
    nominalSum = getBackgroundSum(rFile, variable, backgroundlist)
    upSum = getBackgroundSum(rFile, variable, backgroundlist, systematic+"Up")
    downSum = getBackgroundSum(rFile, variable, backgroundlist, systematic+"Down")

    print "    Setting style"
    setStyle(nominalSum, ROOT.kBlack, "MEM discriminan", "Events")
    setStyle(upSum, ROOT.kRed, "MEM discriminan", "Events")
    setStyle(downSum, ROOT.kBlue, "MEM discriminan", "Events")

    print "    Get Ratio"
    RefRatio, Ratios = getRatioPlot(nominalSum, [upSum, downSum])

    canvas = getCanvas("c1", ratio = True)

    orderedHistoList = [(nominalSum, "histoe"), (upSum, "histoe"), (downSum, "histoe")]
    orderedRatioList = [(RefRatio, "histoe"), (Ratios[0], "P"), (Ratios[1], "P")]

    print "    Drawing plot"
    drawHistos(orderedHistoList, canvas = canvas, orderedRatioList = orderedRatioList)

    print "    Making Legend"
    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    leg.AddEntry(nominalSum, "Nominal", "l")
    leg.AddEntry(upSum, systematic+"Up", "l")
    leg.AddEntry(downSum, systematic+"Down", "l")
    leg.Draw("same")

    canvas.Print("testout.pdf")


if __name__ == "__main__":
    inputfile = "/Users/korbinianschweiger/Code/data/ttH/sparseHistos/V25_lepVetoLoose_systematics_v1_topPt/merged_SR_ddQCD.root"

    bkgs = ["ddQCD", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar",
            "ttbarOther", "wjets", "zjets", "diboson", "stop", "ttw", "ttz"]

    cat = "j8t4"

    systematic = "CMS_ttH_CSVhf"

    makeSystComparison(inputfile, cat, bkgs, systematic)
