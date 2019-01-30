"""
Module for making easy and fast ratio plots

Usage: 
1.) Initialize the RatioPlot class with a name (so the canvas has a unique name)
2.) Add the list of histograms that you want in the plot with the addHistos method.
    The fist will be used as the reference histogram (and the line in the ratio)
3.) Run the drawPlot method and pass a list of legend labels in the order of the
    histograms passed with the addHistos method. Passing a xTitle is optional. Otherwise
    the one of the leading histogram is used.
"""
import logging
from copy import deepcopy

import ROOT


class RatioPlot(object):
    """
    Class for making nice and fast ratio plots
    """
    def __init__(self, name, width=640, height=580):
        logging.debug("Initializing class")
        self.canvas = ROOT.TCanvas("canvas_"+str(name),"canvas_"+str(name),width, height)
        self.canvas.Divide(1,2)
        self.canvas.cd(1).SetPad(0.,0.3-0.02,1.0,0.975)
        self.canvas.cd(2).SetPad(0.,0.0,1.0,0.3*(1-0.02))
        self.canvas.cd(1).SetBottomMargin(0.02)
        self.canvas.cd(2).SetTopMargin(0.00)
        self.canvas.cd(2).SetTicks(1,1)
        self.canvas.cd(1).SetTicks(1,1)
        self.canvas.cd(2).SetFillStyle(0)
        self.canvas.cd(1).SetFillStyle(0)
        self.canvas.cd(2).SetFillColor(0)
        self.canvas.cd(2).SetFrameFillStyle(4000)
        self.canvas.cd(1).SetTopMargin(0.01)
        self.canvas.cd(1).SetRightMargin(0.04)
        self.canvas.cd(1).SetLeftMargin(0.11)
        self.canvas.cd(2).SetRightMargin(0.04)
        self.canvas.cd(2).SetLeftMargin(0.11)
        self.canvas.cd(2).SetBottomMargin(0.3)

        self.histos = None
        self.ratioRange = (0.2,1.8)
        self.ratioText = "#frac{Data}{MC}"
        self.legendSize = (0.7,0.6,0.9,0.8)
        self.labels = None
        self.yTitle = "Events"

    def passHistos(self, ListOfHistos, normalize = False):
        self.histos = ListOfHistos
        if normalize:
            self.yTitle = "Normalized Units"
            for h in self.histos:
                h.Scale(1/h.Integral())

    def addLabel(self, labelText):
        pass

    def addCMSLabel(self):
        cms = ROOT.TLatex( 0.1, 0.8 , '#scale['+str((1)+0.2)+']{#bf{CMS}} #scale['+str((1))+']{#it{simulation}}')
        cms.SetTextFont(42)
        cms.SetTextSize(0.045)
        cms.SetNDC()

        self.labels.append(cms)
        
    def drawPlot(self, legendText, xTitle = None):
        maximimus = []
        minimums = []
        for h in self.histos:
            maximimus.append(h.GetMaximum())

        leg = ROOT.TLegend(self.legendSize[0], self.legendSize[1], self.legendSize[2], self.legendSize[3])
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.05)
        ################################################
        # Making main plot
        self.canvas.cd(1)
        for ihisto, histo in enumerate(self.histos):
            if ihisto == 0:
                histo.Draw("histoe")
                histo.SetMaximum(max(maximimus)*1.15)
                histo.SetMinimum(0)
                histo.SetTitle("")
                histo.GetYaxis().SetTitle(self.yTitle)
                histo.GetXaxis().SetTitleSize(0)
                histo.GetXaxis().SetLabelSize(0)
                histo.GetYaxis().SetTitleOffset(0.66)
                histo.GetYaxis().SetTitleSize(0.06)
            else:
                histo.Draw("histoesame")
            leg.AddEntry(histo, legendText[ihisto], "PLE")
        leg.Draw("same")
        if self.labels is not None:
            for label in self.labels:
                label.Draw("same")
        ################################################
        # Making ratio plot
        self.canvas.cd(2)
        ratios = self._makeAllRatios()
        assert len(ratios) == len(self.histos)
        for iratio, ratio in enumerate(ratios):
            if iratio == 0:
                ratio.SetTitle("")
                ratio.GetXaxis().SetTitleOffset(0.8)
                ratio.GetXaxis().SetTitleSize(0.125)
                ratio.GetXaxis().SetLabelSize(ratio.GetYaxis().GetLabelSize()*1.2)
                ratio.GetYaxis().SetTitleOffset(0.4)
                ratio.GetYaxis().SetTitleSize(0.1)
                ratio.GetYaxis().CenterTitle()
                if xTitle is not None:
                    ratio.GetXaxis().SetTitle(xTitle)
                ratio.GetYaxis().SetTitle(self.ratioText)
                ratio.Draw("histo")
            else:
                ratio.Draw("sameP")
                
        return deepcopy(self.canvas)
                
    def _makeAllRatios(self):
        ListOfRatios = []
        for ihisto, histo in enumerate(self.histos):
            logging.info("Make ratio for %s", histo.GetName())
            if ihisto == 0:
                logging.debug("Creating ratio line")
                ListOfRatios.append(self._makeRatioLine(histo))
            else:
                logging.debug("Creation ratio")
                ListOfRatios.append(self._makeRatio(histo, self.histos[0])[0])
        return ListOfRatios

    def _makeRatioLine(self, histo):
        l = histo.Clone()
        l.SetName("ratioline_"+l.GetName())
        l.SetTitle("")
        l.Divide(histo)
        l.SetLineColor(1)
        l.SetLineStyle(2)
        l.SetLineWidth(1)
        l.SetFillStyle(0)
        lowerbound, upperbound = self.ratioRange
        l.GetYaxis().SetRangeUser(lowerbound, upperbound)
        l.GetYaxis().SetTitle(self.ratioText)
        l.GetYaxis().SetTitleOffset(1.1)
        l.GetXaxis().SetTitleOffset(0.9)
        l.GetXaxis().SetLabelSize(histo.GetXaxis().GetLabelSize()*(1/0.4))
        l.GetYaxis().SetLabelSize(histo.GetYaxis().GetLabelSize()*(1/0.4))
        l.GetXaxis().SetTitleSize(histo.GetXaxis().GetTitleSize()*(1/0.4))
        l.GetYaxis().SetTitleSize(histo.GetYaxis().GetTitleSize()*(1/0.4))
        l.GetYaxis().SetNdivisions(505)
        l.GetXaxis().SetNdivisions(510)
        #print l.GetXaxis().GetLabelSize()
        for i in range(l.GetNbinsX()+1):
            l.SetBinContent(i,1)
            l.SetBinError(i,0)
        logging.debug("Ratio line generated: "+str(l))
        return deepcopy(l)

    def _makeRatio(self, h, href):
        logging.debug("Making ratio for ratio plot from "+str(h))
        grref = ROOT.TGraphAsymmErrors(href)
        ratio = grref.Clone("ratio_"+h.GetName())
        ratio.SetMarkerColor(h.GetLineColor())
        ratio.SetLineColor(h.GetLineColor())
        x, y = ROOT.Double(0), ROOT.Double(0)
        mindiv = 9999.
        maxdiv = -9999.
        for i in range(0,grref.GetN()):
            grref.GetPoint(i, x, y)
            currentBin = h.FindBin(x)
            currentBinContent = h.GetBinContent(currentBin)
            if currentBinContent > 0:
                if y != 0:
                    ratioval = currentBinContent/y
                else:
                    ratioval = 0
                ratio.SetPoint(i, x, ratioval)
                if ratioval > maxdiv and ratioval > 0:
                    maxdiv = round(ratioval, 1)
                if ratioval < mindiv and ratioval > 0:
                    mindiv = round(ratioval, 1)
            else:
                ratio.SetPoint(i, x, -999)

            if y > 0:
                if currentBinContent > 0:
                    ratio.SetPointEYlow(i, grref.GetErrorYlow(i)/currentBinContent)
                    ratio.SetPointEYhigh(i, grref.GetErrorYhigh(i)/currentBinContent)
                else:
                    ratio.SetPointEYlow(i, 1-(y-grref.GetErrorYlow(i))/y)
                    ratio.SetPointEYhigh(i, (y+grref.GetErrorYhigh(i))/y-1)
            else:
                ratio.SetPointEYlow(i, 0)
                ratio.SetPointEYhigh(i, 0)
        return [deepcopy(ratio), mindiv, maxdiv]
