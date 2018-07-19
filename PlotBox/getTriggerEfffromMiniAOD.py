import time
import ROOT
import os
import yaml
from collections import OrderedDict

from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

def checkTriggerIndex(name,index, names):
    if not 'firstTriggerError' in globals():
        global firstTriggerError
        firstTriggerError = True
    if index>=names.size():
        if firstTriggerError:
            for tr in names: print tr
            print
            print name," not found!"
            print
            firstTriggerError = False
            return False
        else:
            return False
    else:
        return True

def expandJSON(fileName):
    with open(fileName, 'r') as f:
        LSfromFile = yaml.safe_load(f) #json loads all entries as unicode (u'..')
    expandedJSON = {}
    for run in LSfromFile:
        expandedLS = []
        for block in LSfromFile[run]:
            firstLS, secondLS = block[0], block[1]
            for i in range(firstLS, secondLS+1):
                expandedLS.append(i)
        expandedJSON[run] = set(expandedLS)

    return expandedJSON

    
#collections MiniAOD
jetCollection = "slimmedJets"
muonCollection = "slimmedMuons"
electronCollection = "slimmedElectrons"
triggerResults = "TriggerResults::HLT"

def loopMiniAOD(files, hnum, hdenom, hnLS, Triggers2Save, maxEvents = -1, isMC = False, jsonFile = None):
    t0 = time.time()
    
    expJSON = None
    if jsonFile is not None:
        expJSON = expandJSON(jsonFile)
    
    
    eventsOff = Events(files)
    offJets_source, offJets_label = Handle("vector<pat::Jet>"), (jetCollection)
    offEle_source, offEle_label = Handle("vector<pat::Electron>"), (electronCollection)
    offMu_source, offMu_label = Handle("vector<pat::Muon>"), (muonCollection)
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), (triggerResults)
    if isMC:
        pileUp_source, pileUp_label = Handle("vector<PileupSummaryInfo>"), ("slimmedAddPileupInfo")
    tdiff = time.time()
    evtsProcessed = 0

    prevLS = 0
    prevLS2 = 0
    for i,event in enumerate(eventsOff):
        if i%10000==0 and i != 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(i, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()
        if maxEvents != -1 and i >= maxEvents:
            break
        lumi = event.eventAuxiliary().luminosityBlock()
        
        inJSON = False
        if expJSON is not None:
            evt = event.eventAuxiliary().event()
            run = event.eventAuxiliary().run()
            if str(run) in expJSON.keys():
                if lumi in expJSON[str(run)]:
                    inJSON = True

        LSInJSON = True
        if not inJSON and expJSON is not None:
            if prevLS2 != lumi:
                print run, lumi, "not in JSON"
                prevLS2 = lumi
            LSInJSON = False
            continue

        if prevLS != lumi:
            print "At a new LS {0} (previous {1})".format(lumi,prevLS)
            prevLS = lumi

            if LSInJSON:
                hnLS.Fill(0.5)

        
        event.getByLabel(offJets_label, offJets_source)
        event.getByLabel(offEle_label, offEle_source)
        event.getByLabel(offMu_label, offMu_source)
        event.getByLabel(triggerBitLabel, triggerBits)
        
        if isMC:
            event.getByLabel(pileUp_label, pileUp_source)

        var2Fill = 0
        ht = 0
        nJets = 0
        for jet in offJets_source.product():
            if jet.pt() > 30 and abs(jet.eta()) < 2.4:
                nJets += 1
                ht += jet.pt()

        var2Fill = ht
            
        names = event.object().triggerNames(triggerBits.product())
        triggerspassing = []
        Tresults = {}
        names = event.object().triggerNames(triggerBits.product())
        triggerNames = names.triggerNames()
        for i,triggerName in enumerate(triggerNames):
            if triggerName.split("_v")[0] in Triggers2Save:
                index = names.triggerIndex(triggerName)
                if checkTriggerIndex(triggerName,index,names.triggerNames()):
                    if triggerBits.product().accept(index):
                        Tresults[triggerName.split("_v")[0]] = 1
                    else:
                        Tresults[triggerName.split("_v")[0]] = 0

        if Tresults[Triggers2Save[0]] == 1:
            hdenom.Fill(var2Fill)
        if Tresults[Triggers2Save[1]] == 1 and Tresults[Triggers2Save[0]] == 1:
            hnum[0].Fill(var2Fill)
        if Tresults[Triggers2Save[2]] == 1 and Tresults[Triggers2Save[0]] == 1:
            hnum[1].Fill(var2Fill)
        if Tresults[Triggers2Save[3]] == 1 and Tresults[Triggers2Save[0]] == 1:
            hnum[2].Fill(var2Fill)
        if Tresults[Triggers2Save[4]] == 1 and Tresults[Triggers2Save[0]] == 1:
            hnum[3].Fill(var2Fill)
        if Tresults[Triggers2Save[5]] == 1 and Tresults[Triggers2Save[0]] == 1:
            hnum[4].Fill(var2Fill)

    print "Events processed: {0}".format(i)
    print "Total time MiniAOD: {0:8f}".format(time.time()-t0)
    return evtsProcessed   


def getHistograms(miniAOD_File, outputfile = "miniAODTriggerEfficiency", maxEvents = -1):
    json = None#"/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"
    #######################
    hDenominator = ROOT.TH1F("hdenom","hdenom",50,500,2500)
    #######################
    hNumerator1 = ROOT.TH1F("hnum_HT1050","hnum_HT1050",50,500,2500)
    hNumerator2 = ROOT.TH1F("hnum_Jet500","hnum_Jet500",50,500,2500)
    hNumerator3 = ROOT.TH1F("hnum_6j1t","hnum_6j1t",50,500,2500)
    hNumerator4 = ROOT.TH1F("hnum_6j2t","hnum_6j2t",50,500,2500)
    hNumerator5 = ROOT.TH1F("hnum_4j3t","hnum_4j3t",50,500,2500)
    hNumerator = [hNumerator1, hNumerator2, hNumerator3, hNumerator4, hNumerator5]
    #######################
    hnLS = ROOT.TH1F("hnLS","hnLS",1,0,1)
    #######################
    trigger = ["HLT_IsoMu27",
               "HLT_PFHT1050",
               "HLT_PFJet500",
               "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5",
               "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
               "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0"]
    #######################

    loopMiniAOD(miniAOD_File, hNumerator, hDenominator, hnLS, trigger, maxEvents, jsonFile = json)

    #print hNumerator.Integral(), hDenominator.Integral()
    #gr = ROOT.TGraphAsymmErrors(hNumerator, hDenominator)
    #gr.Draw()
    of = ROOT.TFile(outputfile+".root","RECREATE")
    of.cd()
    #gr.Write()
    for h in hNumerator:
        h.Write()
    hDenominator.Write()
    hnLS.Write()
    of.Close

if __name__ == "__main__":
    miniAOD_File = ["root://cms-xrd-global.cern.ch//store/data/Run2017C/SingleMuon/MINIAOD/31Mar2018-v1/910000/BE068F10-3D38-E811-A58C-FA163E152BEF.root",
                    #"root://cms-xrd-global.cern.ch//store/data/Run2017C/SingleMuon/MINIAOD/31Mar2018-v1/90000/FE63323C-3137-E811-899A-FA163E35E61A.root"
    ]
    
    getHistograms(miniAOD_File)
