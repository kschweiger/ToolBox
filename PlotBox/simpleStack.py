import ROOT
#ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

data = [("data","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/data.root","1",1,1,ROOT.kBlack,)]
signal = [("tth","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root","",0.293,3298133.74764,ROOT.kBlue)]
backgrounds =  [("ttother", "/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC967990ee1195/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root","ttCls<40",373.3,42319656,ROOT.kRed-7),
                ("ttcc","/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC967990ee1195/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root","ttCls>40 && ttCls<46",373.3,42319656,ROOT.kRed+1),
                ("ttb","/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC967990ee1195/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root","ttCls==51",373.3,42319656,ROOT.kRed-2),
                ("tt2b","/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC967990ee1195/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root","ttCls==52",373.3,42319656,ROOT.kRed+2),
                ("ttbb","/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC967990ee1195/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root","ttCls>52",373.3,42319656,ROOT.kRed+3),
                ("qcd2000","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.root","1",20.54,5321638.0,ROOT.kGreen-8),
                ("qcd1500","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.root","1",101.8,11013774.0,ROOT.kSpring+8),
                ("qcd1000","/mnt/t3nfs01/data01/shome/koschwei/tth/gc/projectSkimFH/GC8d44c2156b97/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.root","1",1005.0,14051171.0,ROOT.kGreen+4),
                ("qcd700","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.root","1",5962.0,42883344.0,ROOT.kGreen+3),
                ("qcd500","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8.root","1",29070.0,51353952.0,ROOT.kGreen+2),                
                ("qcd300","/scratch/koschwei/ttH/skims/2017/ttH_AH_v1/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8.root","1",311900.0,59618096.0,ROOT.kGreen+1),                
]
var = "Sum$(jets_pt/jets_corr_JER > 0)"
#var = "Sum$(jets_pt > 0)"
vard = "Sum$(jets_pt > 0)"
binning = (50,50,550)
binning = (20,500,2500)
binning = (5,5.5,10.5)
genSel = "HLT_ttH_FH && jets_pt[5]>40  && nBCSVM >= 2 && numJets >= 6 && ht30>500"
stackinit = False
bgsum = None
stack = ROOT.THStack("bg","")
histos = {}
files = {}

name, path, sel, xsec, ngen, color = data[0]    
files[name] = ROOT.TFile(path, "READ")
tree = files[name].Get("tree")
histos[name] = ROOT.TH1F("h_"+name,"h_"+name,binning[0],binning[1],binning[2])
nSel = tree.Project("h_"+name, vard, "(" + genSel + " && " + sel +  ")")
print "Data",nSel
histos[name].SetLineColor(ROOT.kAzure+5)
histos[name].SetMarkerColor(ROOT.kAzure+5)
#histos[name].SetMarkerSize(2)
histos[name].SetMarkerStyle(21)


for bg in backgrounds:
    name, path, sel, xsec, ngen, color = bg
    #print "Adding",name
    files[name] = ROOT.TFile(path,"READ")
    tree = files[name].Get("tree")
    histos[name] = ROOT.TH1F("h_"+name,"h_"+name,binning[0],binning[1],binning[2])
    histos[name].SetFillColor(color)
    histos[name].SetFillStyle(1001)
    #print "(" + genSel + " && " + sel +  ")"
    sf = (1000 * xsec * float(41.29)) / float(ngen)
    weight = "( "+str(sf)+" * puWeight * (sign(genWeight)))"
    print 1000,xsec ,41.29,ngen,sf,weight
    npass = tree.Project("h_"+name, var, "(" + genSel + " && " + sel +  ") * "+weight)
    #print "Passing:",npass
    #print histos[name].GetEntries()
    #histos[name].Scale(sf)
    print name,"---- Real events {0} and scaled {1}".format(npass, histos[name].Integral())

    stack.Add(histos[name])
    #print bgsum
    #if not stackinit:
    #    bgsum = histos[name].Clone()
    #    bgsum.SetName("bgsum")
    #    stackinit = True
    #else:
    #    bgsum.Add(histos[name].Clone())
    #print bgsum
    #rfile.Close()

for histo in histos:
    print histos[histo], histos[histo].GetName()


    
c1 = ROOT.TCanvas("c1","c1",1600,1200)
c1.SetLogy()
c1.cd()
stack.Draw("histo")
stack.SetMinimum(1)
histos["data"].Draw("Psame")
c1.Update()
c1.Print("simpleStack_njet.pdf","pdf")

