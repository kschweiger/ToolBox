import ROOT

def moveOverUnderFlow(histo, moveOverFlow=True, moveUnderFlow=True):
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

def moveOverUnderFlow2D(histo, moveOverFlow=True, moveUnderFlow=True):
    nBinsX = histo.GetNbinsX()
    nBinsY = histo.GetNbinsY()


    if moveUnderFlow:
        #Fist move overflow from the bins where one values was inside the histogram
        for iY in range(1,nBinsY+1):
            newBinContent = histo.GetBinContent(0,iY) + histo.GetBinContent(1,iY)
            histo.SetBinContent(1,iY, newBinContent)
            histo.SetBinContent(0,iY, 0)

        for iX in range(1,nBinsX+1):
            newBinContent = histo.GetBinContent(iX,0) + histo.GetBinContent(iX,1)
            histo.SetBinContent(iX,1, newBinContent)
            histo.SetBinContent(iX,0, 0)

        #Move the "corner" bins <-> where both values where outside the histgram
        newBinContent = histo.GetBinContent(0,0) + histo.GetBinContent(1,1)
        histo.SetBinContent(1,1, newBinContent)
        histo.SetBinContent(0, 0, 0)
        newBinContent = histo.GetBinContent(0,nBinsY+1) + histo.GetBinContent(1,nBinsY)
        histo.SetBinContent(1,nBinsY, newBinContent)
        histo.SetBinContent(0,nBinsY+1, 0)

    if moveOverFlow:
        #Fist move overflow from the bins where one values was inside the histogram
        for iY in range(1,nBinsY+1):
            newBinContent = histo.GetBinContent(nBinsX+1,iY) + histo.GetBinContent(nBinsX,iY)
            histo.SetBinContent(nBinsX,iY, newBinContent)
            histo.SetBinContent(nBinsX+1,iY, 0)

        for iX in range(1,nBinsX+1):
            newBinContent = histo.GetBinContent(iX,nBinsY+1) + histo.GetBinContent(iX,nBinsY)
            histo.SetBinContent(iX,nBinsY, newBinContent)
            histo.SetBinContent(iX,nBinsY+1, 0)

        #Move the "corner" bins <-> where both values where outside the histgram
        newBinContent = histo.GetBinContent(nBinsX+1,nBinsY+1) + histo.GetBinContent(nBinsX,nBinsY)
        histo.SetBinContent(nBinsX,nBinsY, newBinContent)
        histo.SetBinContent(nBinsX+1,nBinsY+1, 0)
        newBinContent = histo.GetBinContent(nBinsX+1,0) + histo.GetBinContent(nBinsX,1)
        histo.SetBinContent(nBinsX,1,newBinContent)
        histo.SetBinContent(nBinsX+1,0, 0)
