import ROOT
#########################################################################################################################################
#########################################################################################################################################
base = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/"
#datasetfile = base+"ttH_AH_v1/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.txt"
#datasetfile = base+"May2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.txt"
#datasetfile = base+"ttH_AH_v1/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt"
datasetfile = base+"ttH_AH_TriggerSF_v1/SingleMuon.txt"
#datasetfile = base+"ttH_AH_v1/JetHT.txt"
isData = True
nFiles = -1
#########################################################################################################################################
#########################################################################################################################################with open(datasetfile) as f:
#########################################################################################################################################
with open(datasetfile) as f:
    lines = f.read()

lines = lines.split("\n")

rfilenames = []
summe = 0
nsum = 0
for line in lines:
    a = line.split(" = ")
    if len(a) == 2:
        rfilenames.append(a[0])


filePrefix = {"RunB" : "180711_073213",
              "RunC" : "180711_073305",
              "RunD" : "180711_073423",
              "RunE" : "180711_072958",
              "RunF" : "180711_073345"}

ensureRun = "RunC"
fadded = 0
tree = ROOT.TChain("nanoAOD/Events")
for ifile, f in enumerate(rfilenames):
    if ensureRun != "":
        if filePrefix[ensureRun] not in f:
            continue
    if fadded >= nFiles and nFiles != -1:
        break
    #print "Adding:",f
    tree.Add(f)
    fadded += 1
print "===================================================================================================="
print "=================================== Added {0} files".format(fadded)
#Efficiency of the 6j1t path w.r.t HLT_IsoMu27 || HLT_IsoMu24_eta2p1 (run on SingleMuon sample)
"""
hdenom = ROOT.TH1F("hHTdenom","hHTdenom",10,600,2100)
hnum = ROOT.TH1F("hHTnum","hHTnum",10,600,2100)
nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4  && Jet_jetId >= 2 && Jet_puId >= 4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4 && Jet_jetId >= 2 && Jet_puId >= 4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4 && Jet_jetId >= 2 && Jet_puId >= 4) > 1 &&(HLT_IsoMu27 || HLT_IsoMu24_eta2p1) && run >= 301000")
nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4 && Jet_jetId >= 2 && Jet_puId >= 4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4 && Jet_jetId >= 2 && Jet_puId >= 4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4 && Jet_jetId >= 2 && Jet_puId >= 4) > 1 &&HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)&& run >= 301000")

#nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
#nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
print nNoTrig, nTrig, float(nTrig)/nNoTrig
gr = ROOT.TGraphAsymmErrors(hnum, hdenom)
gr.Draw("AP")
outfile = ROOT.TFile("TriggerEff_6j1t_"+ensureRun+"_ge30100.root","RECREATE")
outfile.cd()
hnum.Write()
hdenom.Write()
gr.Write()
outfile.Close()
raw_input("Press Ret")
"""

#Efficiency of the 6j2t path w.r.t HLT_IsoMu27 || HLT_IsoMu24_eta2p1 (run on SingleMuon sample)
"""
hdenom = ROOT.TH1F("hHTdenom","hHTdenom",10,600,2100)
hnum = ROOT.TH1F("hHTnum","hHTnum",10,600,2100)
nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 1 &&(HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 1 && HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2  && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")

#nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
#nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
print nNoTrig, nTrig, float(nTrig)/nNoTrig
gr = ROOT.TGraphAsymmErrors(hnum, hdenom)
gr.Draw("AP")
outfile = ROOT.TFile("TriggerEff_6j2t_"+ensureRun+".root","RECREATE")
outfile.cd()
hnum.Write()
hdenom.Write()
gr.Write()
outfile.Close()
raw_input("Press Ret")
"""

#Efficiency of the 4j3t path w.r.t HLT_IsoMu27 || HLT_IsoMu24_eta2p1 (run on SingleMuon sample)
"""
hdenom = ROOT.TH1F("hHTdenom","hHTdenom",10,600,2100)
hnum = ROOT.TH1F("hHTnum","hHTnum",10,600,2100)
nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 1 &&(HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 1 && HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")

#nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
#nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 40 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
print nNoTrig, nTrig, float(nTrig)/nNoTrig
gr = ROOT.TGraphAsymmErrors(hnum, hdenom)
gr.Draw("AP")
outfile = ROOT.TFile("TriggerEff_4j3t_"+ensureRun+".root","RECREATE")
outfile.cd()
hnum.Write()
hdenom.Write()
gr.Write()
outfile.Close()
raw_input("Press Ret")
"""


#Efficiency per Run(group) RunC
"""
hdenom = ROOT.TH1F("hHTdenom","hHTdenom",140,299300,302100)
hnum = ROOT.TH1F("hHTnum","hHTnum",140,299300,302100)
nNoTrig = tree.Project("hHTdenom","run", "(HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
nTrig = tree.Project("hHTnum","run", "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
print nNoTrig, nTrig, float(nTrig)/nNoTrig
gr = ROOT.TGraphAsymmErrors(hnum, hdenom)
gr.Draw("AP")
outfile = ROOT.TFile("RunTriggerEff_6j1t_"+ensureRun+".root","RECREATE")
outfile.cd()
hnum.Write()
hdenom.Write()
gr.Write()
outfile.Close()
raw_input("Press Ret")
"""

#Efficiency of the PFHT pr PFJet path w.r.t HLT_IsoMu27 || HLT_IsoMu24_eta2p1 (run on SingleMuon sample)

hdenom = ROOT.TH1F("hHTdenom","hHTdenom",14,600,2000)
hnum = ROOT.TH1F("hHTnum","hHTnum",14,600,2000)
muonSel = "Sum$(Muon_pt > 28 && abs(Muon_eta) < 2.1 && Muon_tightId == 1 && Muon_pfRelIso04_all >= 0.15)"
elVetoSel = " Sum$(Electron_pt > 15 && abs(Electron_eta) < 2.4 && Electron_cutBased >= 2)"
SingleMuSel = "{0} == 1 && {1} == 0".format(muonSel, elVetoSel)
#SingleMuSel = "Muon_pt[0] < 50 && Sum$(FatJet_pt > 200 && abs(FatJet_eta) < 2.4 && FatJet_jetId > 0) > 1 "
nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt > 30 && abs(Jet_eta) < 2.4))", SingleMuSel+" && (HLT_IsoMu27)")
nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt > 30 && abs(Jet_eta) < 2.4))", SingleMuSel+"&& HLT_PFHT1050 && (HLT_IsoMu27)")
#nNoTrig = tree.Project("hHTdenom","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 30 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
#nTrig = tree.Project("hHTnum","Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4))", "Sum$(Jet_pt > 30 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>30 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>30 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT350 && (HLT_IsoMu27 || HLT_IsoMu24_eta2p1)")
print nNoTrig, nTrig, float(nTrig)/nNoTrig
raw_input("Press Ret for plotting")
gr = ROOT.TGraphAsymmErrors(hnum, hdenom)
gr.Draw("AP")
outfile = ROOT.TFile("TriggerEff_HT_jetID_"+ensureRun+".root","RECREATE")
outfile.cd()
hdenom.Write()
hnum.Write()
gr.Write()
outfile.Close()
raw_input("Press Ret")

#Efficiency of the 6j1t path w.r.t to the 6jht part of the path --> b-tagging efficiency (run on JetHT sample)
"""
nNoTrigbeff = tree.Draw("","Sum$(Jet_pt > 60 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>50 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>50 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40")
nTrigbeff =   tree.Draw("","Sum$(Jet_pt > 60 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>50 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>50 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && HLT_PFHT430_SixPFJet40")
print nNoTrigbeff, nTrigbeff, float(nTrigbeff)/nNoTrigbeff
"""
#Efficiency of the ht part of the 6j1t path --> Low stats because HLT_PFHT430 strongly prescaled at L1 (run on JetHTSample)
"""
nNoTrigbeff = tree.Draw("","Sum$(Jet_pt > 60 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>50 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>50 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430")
nTrigbeff =   tree.Draw("","Sum$(Jet_pt > 60 && abs(Jet_eta) < 2.4) >= 6 && Sum$(Jet_pt *(Jet_pt>50 && abs(Jet_eta) < 2.4)) > 600 && Sum$(Jet_btagCSVV2 > 0.8838 && Jet_pt>50 && abs(Jet_eta) < 2.4) > 2 && HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 && HLT_PFHT430")
print nNoTrigbeff, nTrigbeff, float(nTrigbeff)/nNoTrigbeff
"""
