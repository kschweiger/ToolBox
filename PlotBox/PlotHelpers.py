import ROOT
import copy
import logging

def moveOverUnderFlow(histo, moveOverFlow=True, moveUnderFlow=False):
    """
    Function for moving the overflow and (or) underflow bin to the first/last bin
    """
    nBins = histo.GetNbinsX()
    if moveUnderFlow:
        underflow = histo.GetBinContent(0)
        fistBinContent = histo.GetBinContent(1)
        histo.SetBinContent(1, fistBinContent+underflow)
        histo.SetBinContent(0, 0)
    if moveOverFlow:
        overflow = histo.GetBinContent(nBins+1)
        lastBinContent = histo.GetBinContent(nBins)
        histo.SetBinContent(nBins, lastBinContent+overflow)
        histo.SetBinContent(nBins+1, 0)

def saveCanvasListAsPDF(listofCanvases, outputfilename, foldername):
    logging.info("Writing outputfile %s.pdf",outputfilename)
    if len(listofCanvases) > 1:
        for icanvas, canves in enumerate(listofCanvases):
            if icanvas == 0:
                canves.Print(foldername+"/"+outputfilename+".pdf[", "pdf")
                #canves.Print(foldername+"/"+outputfilename+".pdf", "pdf")
                canves.Print(foldername+"/"+outputfilename+".pdf", "pdf")
            elif icanvas == len(listofCanvases)-1:
                canves.Print(foldername+"/"+outputfilename+".pdf", "pdf")
                canves.Print(foldername+"/"+outputfilename+".pdf]", "pdf")
            else:
                canves.Print(foldername+"/"+outputfilename+".pdf", "pdf")
    else:
        listofCanvases[0].Print(foldername+"/"+outputfilename+".pdf", "pdf")

def makeDistribution(prefix, histos, Files, selection, mcWeight, color):
    retHistos = []
    for histo, bins, sBin, eBin in histos:
        logging.info("Processing plot: %s",histo)
        h = ROOT.TH1F(histo+"_"+prefix, histo+"_"+prefix, bins, sBin, eBin)
        h.SetTitle("")
        logging.info("Created histos %s", h)
        h.SetLineColor(color)
        for ifile, file_ in enumerate(Files):
            fileName, xsec, ngen = file_
            logging.info("processing file: %s", fileName.GetName().split("/")[-1])
            #logging.info("processing file: %s", fileName.split("/")[-1])
            #rfile = ROOT.TFile.Open(fileName)
            logging.debug(fileName)
            tree = fileName.Get("tree")
            SelTimesWeight = "({0}) * ({1} * {2})".format(selection, 100000 * (xsec/float(ngen)), mcWeight)
            logging.debug("Selection * weight: %s",SelTimesWeight)
            logging.debug("Variable: %s",histo)
            if ifile == 0:
                logging.debug("Projection initial histo %s", h.GetName())
                nProj = tree.Project(h.GetName(), histo, SelTimesWeight)
                logging.debug("Current histo integral: %s", h.Integral())
            else:
                tmpName = h.GetName()+"_tmp"+str(ifile)
                tmph = h.Clone(tmpName)
                nProj = tree.Project(tmpName, histo, SelTimesWeight)
                logging.debug("Current histo integral: %s", tmph.Integral())
                logging.debug("Adding projected histos")
                h.Add(tmph)
            logging.debug("Projection yielded %s events",nProj)
            logging.debug("Total histo integral: %s", h.Integral())
        moveOverUnderFlow(h)
        retHistos.append(h)

    return copy.deepcopy(retHistos)
