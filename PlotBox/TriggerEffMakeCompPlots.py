import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
t2Files = {"RunC" : ROOT.TFile("TriggerEff_6j2t_RunC.root","READ"),
           "RunD" : ROOT.TFile("TriggerEff_6j2t_RunD.root","READ"),
           "RunE" : ROOT.TFile("TriggerEff_6j2t_RunE.root","READ")}
t1Files = {"RunC" : ROOT.TFile("TriggerEff_6j1t_RunC.root","READ"),
           "RunCge301" : ROOT.TFile("TriggerEff_6j1t_RunC_ge30100.root","READ"),
           "RunD" : ROOT.TFile("TriggerEff_6j1t_RunD.root","READ"),
           "RunE" : ROOT.TFile("TriggerEff_6j1t_RunE.root","READ")}
t3Files = {"RunC" : ROOT.TFile("TriggerEff_4j3t_RunC.root","READ"),
           "RunD" : ROOT.TFile("TriggerEff_4j3t_RunD.root","READ"),
           "RunE" : ROOT.TFile("TriggerEff_4j3t_RunE.root","READ")}

color = {"RunC": ROOT.kGreen+3,
         "RunCge301" : ROOT.kSpring+9,
         "RunD": ROOT.kBlue,
         "RunE": ROOT.kRed}

order = ["RunE","RunD","RunC"]

c1t = ROOT.TCanvas("c1t","c1t",640,580)
c2t = ROOT.TCanvas("c2t","c2t",640,580)
c3t = ROOT.TCanvas("c3t","c3t",640,580)

leg = ROOT.TLegend(0.1,0.6,0.3,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)


c1t.cd()
for irun, run in enumerate(order+["RunCge301"]):
    gr = t1Files[run].Get("divide_hHTnum_by_hHTdenom")
    gr.SetMarkerColor(color[run])
    gr.SetLineColor(color[run])
    if irun == 0:
        options = "AP"
        gr.SetTitle("HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5")
    else:
        options = "P"
    gr.Draw(options)
    leg.AddEntry(gr, run, "PLE")
leg.Draw("same")
c1t.Update()
c1t.SaveAs("EffCompt_6j1t.pdf")

leg2 = ROOT.TLegend(0.1,0.6,0.3,0.9)
leg2.SetFillStyle(0)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.05)

c2t.cd()
for irun, run in enumerate(order):
    gr = t2Files[run].Get("divide_hHTnum_by_hHTdenom")
    gr.SetMarkerColor(color[run])
    gr.SetLineColor(color[run])
    if irun == 0:
        options = "AP"
        gr.SetTitle("HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2")
    else:
        options = "P"
    gr.Draw(options)
    leg2.AddEntry(gr, run, "PLE")
leg2.Draw("same")
c2t.Update()
c2t.SaveAs("EffCompt_6j2t.pdf")


    
c3t.cd()
for irun, run in enumerate(order):
    gr = t3Files[run].Get("divide_hHTnum_by_hHTdenom")
    gr.SetMarkerColor(color[run])
    gr.SetLineColor(color[run])
    if irun == 0:
        options = "AP"
        gr.SetTitle("HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0")
    else:
        options = "P"
    gr.Draw(options)
leg2.Draw("same")
c3t.Update()
c3t.SaveAs("EffCompt_4j3t.pdf")

    
