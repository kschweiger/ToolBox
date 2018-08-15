import ROOT

path = "Trigger_plots_runDep_v2/"
runfiles = [
    ("RunB","2Dhistis_eff_runDep_tightCutRunB_all_plusHTplusJet_wPuGenB_binningv2.root"),
    ("RunC","2Dhistis_eff_runDep_tightCutRunCNoPre_all_plusHTplusJet_wPuGenB_binningv2.root"),
    ("RunD","2Dhistis_eff_runDep_tightCutRunD_all_plusHTplusJet_wPuGenB_binningv2.root"),
    ("RunE","2Dhistis_eff_runDep_tightCutRunE_all_plusHTplusJet_wPuGenB_binningv2.root"),
    ("RunF","2Dhistis_eff_runDep_tightCutRunF_all_plusHTplusJet_wPuGenB_binningv2.root"),
]

vars_ = ["pt","nb","ht"]

trees = {}
files = {}
histos = {}
for r,f in runfiles:
    files[r] = ROOT.TFile(path+f,"READ")
    histos[r] = {}
    for v in vars_:
        histos[r][v] = files[r].Get("hData_eff_"+v)


print histos[r][v]
