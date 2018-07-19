import ROOT

miniFile = ROOT.TFile("/mnt/t3nfs01/data01/shome/koschwei/ToolBox/PlotBox/gc/GC9fe2ed79d254/SingleMuon_RunC2017.root","READ")
tthbb13File = ROOT.TFile("/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1/SingleMuon.root", "READ")

tree = tthbb13File.Get("tree")


#ttHbb13 plots:
hdenom_ttH = ROOT.TH1F("hdenom_ttH","hdenom_ttH",50,500,2500)
hnum_ttH = ROOT.TH1F("hnum_ttH","hnum_ttH",50,500,2500)

hdenom_ttH.SetLineColor(ROOT.kGreen+2)
hnum_ttH.SetLineColor(ROOT.kGreen+2)

print "Projection denominator"
tree.Project("hdenom_ttH","ht30","HLT_BIT_HLT_IsoMu27 && (run>= 299337 && run<= 302029)")
print "Projection Numerator"
tree.Project("hnum_ttH","ht30","HLT_BIT_HLT_IsoMu27 && HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 && (run>= 299337 && run<= 302029)")

gr_ttH = ROOT.TGraphAsymmErrors(hnum_ttH, hdenom_ttH)
gr_ttH.SetLineColor(ROOT.kGreen+2)
gr_ttH.SetMarkerColor(ROOT.kGreen+2)
gr_ttH.SetMaximum(0.3)

#MiniAOD plots
print "Getting miniAOD histos"
hdenom_mini = miniFile.Get("hdenom")
hnum_mini = miniFile.Get("hnum_6j2t")

hdenom_mini.SetLineColor(ROOT.kBlue)
hnum_mini.SetLineColor(ROOT.kBlue)


gr_mini = ROOT.TGraphAsymmErrors(hnum_mini, hdenom_mini)
gr_mini.SetLineColor(ROOT.kBlue)
gr_mini.SetMarkerColor(ROOT.kBlue)
gr_mini.SetMaximum(0.3)
#Actual P[otting

cGraph = ROOT.TCanvas("cGraph","cGraph",640,580)
cDenom = ROOT.TCanvas("cDenom","cDenom",640,580)
cNum = ROOT.TCanvas("cNum","cNum",640,580)


line = ROOT.TF1("line","0.1",0.0,9000.0)

leg = ROOT.TLegend(0.1,0.6,0.4,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)
leg.AddEntry(gr_mini, "MiniAOD", "L")
leg.AddEntry(gr_ttH, "tthbb13", "L")



cGraph.cd()
gr_mini.Draw("AP")
gr_ttH.Draw("PSame")
line.Draw("same")
leg.Draw("same")
cGraph.Update()
cGraph.SaveAs("compTriggerTurnOnMinittHbb13_graphs.pdf")

cDenom.cd()
hdenom_mini.DrawNormalized("histo")
hdenom_ttH.DrawNormalized("histoSame")
leg.Draw("same")
cDenom.Update()
cDenom.SaveAs("compTriggerTurnOnMinittHbb13_denom.pdf")


cNum.cd()
hnum_mini.DrawNormalized("histo")
hnum_ttH.DrawNormalized("histoSame")
leg.Draw("same")
cNum.Update()
cNum.SaveAs("compTriggerTurnOnMinittHbb13_num.pdf")
