import ROOT
import copy

##########################################################################
# Settings
toprocess = 1500000000
#xsec94X = 373.3
#xsec80X = 831.76
xsec94X = 90.578#0.2934045
xsec80X = 831.76#0.2934045

lumi16 = 35.920026
lumi17 = 41.29
nVhbbFiles = 10#800
nNanoFiles = 1#10
skipGenCut = False
##########################################################################

##########################################################################################################
vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
#vhbbDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/pub2017/CMSSW_8_0_26_patch2/src/TTH/MEAnalysis/gc/datasets/T3_V25_lepVetoLoose_systematics_v1/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt"
with open(vhbbDataset) as f:
    lines = f.read()
lines = lines.split("\n")
vhbbInput = []
for line in lines:
    a = line.split(" = ")
    if len(a) == 2:
        vhbbInput.append(a[0])

##########################################################################################################
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_TriggerSF_v1/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.txt"
nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_TriggerSF_v1/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8.txt"
#nanoDataset = "/mnt/t3nfs01/data01/shome/koschwei/tth/2017Data/CMSSW_9_4_6_patch1/src/TTH/MEAnalysis/gc/datasets/ttH_AH_v1/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.txt"
with open(nanoDataset) as f:
    lines = f.read()

lines = lines.split("\n")
nanoInput = []
for line in lines:
    a = line.split(" = ")
    
    if len(a) == 2:
        nanoInput.append(a[0])
##########################################################################################################

vhbbTree = ROOT.TChain("vhbb/tree")
nanoTree = ROOT.TChain("nanoAOD/Events")

for ifile, f in enumerate(vhbbInput):
    if ifile > nVhbbFiles:
        break
    vhbbTree.Add(f)
for ifile, f in enumerate(nanoInput):
    if ifile > nNanoFiles:
        break
    nanoTree.Add(f)

vhbbnEvents = vhbbTree.GetEntries()
nanonEvents = nanoTree.GetEntries()

vhbbTotal = 0
nanoTotal = 0

print vhbbnEvents,nanonEvents

cutorder = ["trigger", "sixJet","sixJetge40", "ht", "2CSVM"]

vhbbcutFlow = {"total" : 0,
               "trigger" : 0,
               "sixJet" : 0,
               "sixJetge40" : 0,
               "ht" : 0,
               "2CSVM": 0}
nanocutFlow = copy.copy(vhbbcutFlow)
print "------------------ VHbb ---------------------"
#vhbb cutflow
nprocessed = 0
for iEv in range(vhbbnEvents):
    vhbbTree.GetEvent(iEv)
    vhbbTotal += 1
    if skipGenCut:
        genCut = True
    else:
        genCut = vhbbTree.nGenWZQuark == 0
        #print vhbbTree.nGenWZQuark, genCut
    if genCut:
        if nprocessed%10000 == 0:
            print "Events processed: ",nprocessed
        nprocessed += 1
        vhbbcutFlow["total"] += 1
        
        if (vhbbTree.HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v == 1 or
            vhbbTree.HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v == 1):
            vhbbcutFlow["trigger"] += 1

            nJet30EtaRes = 0
            j6ge40 = False
            ht30 = 0
            nCSVM = 0
            
            for iJet in range(vhbbTree.nJet):
                if vhbbTree.Jet_pt[iJet] > 30 and abs(vhbbTree.Jet_eta[iJet]) < 2.4:
                    nJet30EtaRes += 1
                    ht30 += vhbbTree.Jet_pt[iJet]
                    if nJet30EtaRes == 6 and vhbbTree.Jet_pt[iJet] > 40:
                        j6ge40 = True  
                    if vhbbTree.Jet_btagCSV[iJet] > 0.8484:
                        nCSVM += 1
            if nJet30EtaRes >= 6:
                vhbbcutFlow["sixJet"] += 1
                if j6ge40:
                    vhbbcutFlow["sixJetge40"] += 1
                    if ht30 > 500:
                        vhbbcutFlow["ht"] += 1
                        if nCSVM >= 2:
                            vhbbcutFlow["2CSVM"] += 1
        if nprocessed >= toprocess:
            break

print "------------------ Nano ---------------------"
#nano cutflow
nprocessed = 0
for iEv in range(nanonEvents):
    nanoTree.GetEvent(iEv)
    nanoTotal += 1
    if nprocessed%10000 == 0:
        print "Events processed: ",nprocessed
    nprocessed += 1
    nanocutFlow["total"] += 1
    if (nanoTree.HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 == 1 or
        nanoTree.HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 == 1 or
        nanoTree.HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0):
        nanocutFlow["trigger"] += 1
        nJet30EtaRes = 0
        j6ge40 = False
        ht30 = 0
        nCSVM = 0
        for iJet in range(nanoTree.nJet):
            if nanoTree.Jet_pt[iJet] > 30 and abs(nanoTree.Jet_eta[iJet]) < 2.4:
                nJet30EtaRes += 1
                ht30 += nanoTree.Jet_pt[iJet]
                if nJet30EtaRes == 6 and nanoTree.Jet_pt[iJet] > 40:
                    j6ge40 = True  
                if nanoTree.Jet_btagCSVV2[iJet] > 0.8838:
                    nCSVM += 1
        if nJet30EtaRes >= 6:
                nanocutFlow["sixJet"] += 1
                if j6ge40:
                    nanocutFlow["sixJetge40"] += 1
                    if ht30 > 500:
                        nanocutFlow["ht"] += 1
                        if nCSVM >= 2:
                            nanocutFlow["2CSVM"] += 1

    if nprocessed >= toprocess:
        break



print vhbbcutFlow
print nanocutFlow

print "------------------ Fractions of total ----------------------"
for key in cutorder:
     vhbbFrac = vhbbcutFlow[key] / float( vhbbcutFlow["total"])
     nanoFrac = nanocutFlow[key] / float( nanocutFlow["total"])
     print "Fraction passing {0} in VHbb: {1}".format(key, vhbbFrac)
     print "Fraction passing {0} in NANO: {1}".format(key, nanoFrac)

print "---------------- Fractions of previous cut-----------------"
prevCut = "total"
for key in cutorder:
     vhbbFrac = vhbbcutFlow[key] / float( vhbbcutFlow[prevCut])
     nanoFrac = nanocutFlow[key] / float( nanocutFlow[prevCut])
     print "Fraction passing {0} in VHbb: {1}".format(key, vhbbFrac)
     print "Fraction passing {0} in NANO: {1}".format(key, nanoFrac)
     prevCut = key

    
print "---------------------------------------------------------------"
print "---------------------------------------------------------------"
print "Total events processing in vhbb:",vhbbTotal
print "Total events processing in NANO:",nanoTotal
print "Scaled to xsec of {0} in VHbb: {1}".format(xsec80X , vhbbcutFlow["2CSVM"] * ( (lumi16 * xsec80X * 1000) /vhbbTotal ))
print "Scaled to xsec of {0} in NANO : {1}".format(xsec94X , nanocutFlow["2CSVM"] * ( (lumi17 * xsec94X * 1000) /nanoTotal ))
print "Scale factor VHbb: lumi *",str( (xsec80X * 1000) /vhbbTotal )
print "Scale factor NANO: lumi *",str( (xsec94X * 1000) /nanoTotal )
print "Trigger Efficiency in VHbb {0}".format( vhbbcutFlow["trigger"]/ float(vhbbcutFlow["total"]))
print "Trigger Efficiency in NANO {0}".format( nanocutFlow["trigger"]/ float(nanocutFlow["total"]))
print "Presel Efficiency after trigger in VHbb {0}".format( vhbbcutFlow["2CSVM"]/ float(vhbbcutFlow["trigger"]))
print "Presel Efficiency after trigger in NANO {0}".format( nanocutFlow["2CSVM"]/ float(nanocutFlow["trigger"]))
print "Sample Efficiency after trigger in VHbb {0}".format( vhbbcutFlow["2CSVM"]/ float(vhbbcutFlow["total"]))
print "Sample Efficiency after trigger in NANO {0}".format( nanocutFlow["2CSVM"]/ float(nanocutFlow["total"]))
