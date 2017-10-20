import ROOT
import collections

luminosity = 35.920026

colors = { "Multijet": 9007, "qcd": 9007,
           "ttH_hbb": 9001,
           "ttbarPlusBBbar": 9002,
           "ttbarPlus2B": 9003,
           "ttbarPlusB" : 9004,
           "ttbarPlusCCbar": 9005,
           "ttbarOther": 9006,
           "ttH_nonhbb": 9008,
           "wjets": 9009,
           "zjets":9010,
           "diboson":9011,
           "stop":9012,
           "ttv":9013, "ttw":9013, "ttz":9013,
           "JetHT": 1,
           "TTbar_inc": ROOT.kRed+2}
#histogram colors (index, r, b, g)
col_tth     = ROOT.TColor(colors["ttH_hbb"], 44/255., 62/255., 167/255.)
col_qcd     = ROOT.TColor(colors["Multijet"], 102/255., 201/255., 77/255.)
col_ttbarBB = ROOT.TColor(colors["ttbarPlusBBbar"], 102/255., 0/255., 0/255.)
col_ttbar2B = ROOT.TColor(colors["ttbarPlus2B"], 80/255., 0/255., 0/255.)
col_ttbarB  = ROOT.TColor(colors["ttbarPlusB"], 153/255., 51/255., 51/255.)
col_ttbarCC = ROOT.TColor(colors["ttbarPlusCCbar"], 204/255., 2/255., 0/255.)
col_ttbarJJ = ROOT.TColor(colors["ttbarOther"], 251/255., 102/255., 102/255.)
col_tthnon  = ROOT.TColor(colors["ttH_nonhbb"], 90/255., 115/255., 203/255.)
col_wjets   = ROOT.TColor(colors["wjets"], 254/255., 195/255., 8/255.)
col_zjets   = ROOT.TColor(colors["zjets"], 191/255., 193/255., 222/255.)
col_diboson = ROOT.TColor(colors["diboson"], 229/255., 198/255., 218/255.)
col_stop    = ROOT.TColor(colors["stop"], 235/255., 73/255., 247/255.)
col_ttv     = ROOT.TColor(colors["ttv"], 246/255., 236/255., 145/255.)

legnames = { "ddQCD": "ddQCD",
             "qcd": "qcd MC",
             "ttH_hbb": "t#bar{t}H(bb)",
             "ttH_nonhbb": "t#bar{t}H(non)",
             "ttbarPlusBBbar": "t#bar{t}+b#bar{b}",
             "ttbarPlus2B": "t#bar{t}+2b",
             "ttbarPlusB" : "t#bar{t}+b",
             "ttbarPlusCCbar": "t#bar{t}+c#bar{c}",
             "ttbarOther": "t#bar{t}+lf",
             "wjets": "W+jets",
             "zjets": "Z+jets",
             "diboson": "diboson",
             "stop": "single top",
             "ttv": "t#bar{t}+V",
             "ttz": "t#bar{t}+V",
             "JetHT": "data",
             "TTbar_inc": "t#bar{t}+jets"}

datasets = collections.OrderedDict([
    ("JetHT","JetHT"),
    ("ttH_hbb","ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
    ("ttH_nonhbb","ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
    ("TTbar_inc","TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"),
    ("QCD300","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD500","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD700","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD1000","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD1500","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("QCD2000","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("ww","WW_TuneCUETP8M1_13TeV-pythia8"),
    ("wz","WZ_TuneCUETP8M1_13TeV-pythia8"),
    ("zz","ZZ_TuneCUETP8M1_13TeV-pythia8"),
    ("st_t","ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin"),
    ("stbar_t","ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin"),
    ("st_s_inc","ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8"),
    ("st_tw","ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
    ("stbar_tw","ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
    ("ttw_wqq","TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
    ("ttz_zqq","TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"),
    ("WJetsToQQ600","WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
    ("WJetsToQQ180","WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8"),
    ("WJetsToQQ180_gencut","WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8"), #gencut, lheHT>400
    ("ZJetsToQQ600","ZJetsToQQ_HT600toInf_13TeV-madgraph"),
    ("WWTo4Q","WWTo4Q_13TeV-powheg"),
    ("ZZTo4Q","ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8"),
    ])

xsecs = { "ttH_hbb": 0.2934045,
    "ttH_nonhbb": 0.2150955,
    "TTbar_inc": 831.76,
    "QCD300": 351300.0,
    "QCD500": 31630.0,
    "QCD700": 6802.0,
    "QCD1000": 1206.0,
    "QCD1500": 120.4,
    "QCD2000": 25.25,
    "ww": 118.7,
    "wz": 47.13,
    "zz": 16.523,
    "st_t": 136.02,
    "stbar_t": 80.95,
    "st_s_inc": 10.32,
    "st_tw": 35.85,
    "stbar_tw": 35.85,
    "ttw_wqq": 0.4062,
    "ttz_zqq": 0.5297,
    "WJetsToQQ600": 95.14,
    "WJetsToQQ180": 2788,
    "WJetsToQQ180_gencut": 343.05, #gencut, lheHT>400
    "ZJetsToQQ600": 5.67,
    "WWTo4Q": 51.723,
    "ZZTo4Q": 7.487
    }

preselection = "HLT_ttH_FH && ht>500 && jets_pt[5]>40"

def get_cuts(systematic=""):
    cuts = {"7j":"numJets{0}==7 && Wmass{0}>60 && Wmass{0}<100".format(systematic),
            "8j":"numJets{0}==8 && Wmass{0}>60 && Wmass{0}<100".format(systematic),
            "9j":"numJets{0}>=9 && Wmass{0}>70 && Wmass{0}<92".format(systematic),
            "3bSR":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.5".format(systematic),
            "4bSR":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.5".format(systematic),
            "3bCR":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.5".format(systematic),
            "4bCR":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.5".format(systematic),
            "3bVR":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bVR":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bCR2":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bCR2":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.5".format(systematic),

            "3bSRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==3 && qg_LR_3b_flavour_5q_0q>0.5",
            "4bSRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)>=4 && qg_LR_4b_flavour_5q_0q>0.5",
            "3bCRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_3b_flavour_5q_0q>0.5",
            "4bCRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_4b_flavour_5q_0q>0.5",
            "3bVRx":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==3 && qg_LR_3b_flavour_5q_0q<0.5",
            "4bVRx":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)>=4 && qg_LR_4b_flavour_5q_0q<0.5",
            "3bCR2x":"nBCSVM==2 && nBCSVL==3 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_3b_flavour_5q_0q<0.5",
            "4bCR2x":"nBCSVM==2 && nBCSVL>=4 && Sum$(jets_btagCSV>0.7)==2 && qg_LR_4b_flavour_5q_0q<0.5",

            "3bSRy":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bSRy":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bCRy":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "4bCRy":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}>0.3 && qg_LR_3b_flavour_5q_0q{0}<0.5".format(systematic),
            "3bVRy":"nBCSVM{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.3".format(systematic),
            "4bVRy":"nBCSVM{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.3".format(systematic),
            "3bCR2y":"nBCSVM{0}==2 && nBCSVL{0}==3 && qg_LR_3b_flavour_5q_0q{0}<0.3".format(systematic),
            "4bCR2y":"nBCSVM{0}==2 && nBCSVL{0}>=4 && qg_LR_4b_flavour_5q_0q{0}<0.3".format(systematic),

}
    return cuts

ttCuts = {"ttbarPlusBBbar": "ttCls>52",
          "ttbarPlus2B": "ttCls==52",
          "ttbarPlusB": "ttCls==51",
          "ttbarPlusCCbar": "ttCls>40 && ttCls<46",
          "ttbarOther": "ttCls<40"}

systematics = ["CMS_res_j",
               #"CMS_scale_j",
               "CMS_scaleAbsoluteStat_j",
               "CMS_scaleAbsoluteScale_j",
               ###"CMS_scaleAbsoluteFlavMap_j", #obsolete (1 anyway)
               "CMS_scaleAbsoluteMPFBias_j",
               "CMS_scaleFragmentation_j",
               "CMS_scaleSinglePionECAL_j",
               "CMS_scaleSinglePionHCAL_j",
               "CMS_scaleFlavorQCD_j",
               "CMS_scaleTimePtEta_j",
               "CMS_scaleRelativeJEREC1_j",
               "CMS_scaleRelativeJEREC2_j",
               "CMS_scaleRelativeJERHF_j",
               "CMS_scaleRelativePtBB_j",
               "CMS_scaleRelativePtEC1_j",
               "CMS_scaleRelativePtEC2_j",
               "CMS_scaleRelativePtHF_j",
               "CMS_scaleRelativeBal_j", #added this one for Moriond 2016/80X
               "CMS_scaleRelativeFSR_j",
               "CMS_scaleRelativeStatFSR_j",
               "CMS_scaleRelativeStatEC_j",
               "CMS_scaleRelativeStatHF_j",
               "CMS_scalePileUpDataMC_j",
               "CMS_scalePileUpPtRef_j",
               "CMS_scalePileUpPtBB_j",
               "CMS_scalePileUpPtEC1_j",
               ###"CMS_scalePileUpPtEC2_j", #always 1
               "CMS_scalePileUpPtHF_j",
               "CMS_ttH_CSVcferr1",
               "CMS_ttH_CSVcferr2",
               "CMS_ttH_CSVhf",
               "CMS_ttH_CSVhfstats1",
               "CMS_ttH_CSVhfstats2",
               "CMS_ttH_CSVjes", ##NEED to include in normal JES!!!
               "CMS_ttH_CSVlf",
               "CMS_ttH_CSVlfstats1",
               "CMS_ttH_CSVlfstats2",
               "CMS_ttH_FHtrigger",
               "CMS_pu",
               #"CMS_ttjetsfsr", #ignore for now
               #"CMS_ttjetsisr"
               "ddQCD_3b",
               "ddQCD_4b"
               ]

normsys = ["lumi_13TeV",
           "pdf_Higgs_ttH",
           "pdf_gg",
           "pdf_qqbar",
           "pdf_qg",
           "QCDscale_ttH",
           "QCDscale_tt",
           "QCDscale_t",
           "QCDscale_V",
           "QCDscale_VV",
           "bgnorm_ttbarPlus2B",
           "bgnorm_ttbarPlusB",
           "bgnorm_ttbarPlusBBbar",
           "bgnorm_ttbarPlusCCbar"]

def create_paves(lumi, data, xlo=0.11, ylo=0.951, xhi=0.95, yhi=1.0):

    pt_lumi = ROOT.TPaveText(xhi-0.25, ylo, xhi, yhi,"brNDC")
    pt_lumi.SetFillStyle(0)
    pt_lumi.SetBorderSize(0)
    pt_lumi.SetFillColor(0)
    pt_lumi.SetTextFont(42)
    pt_lumi.SetTextSize(0.04)
    pt_lumi.SetTextAlign(31) #left=10, bottom=1, centre=2
    pt_lumi.AddText( "{0:.1f}".format(lumi)+" fb^{-1} (13 TeV)" )

    pt_CMS = ROOT.TPaveText(xlo, ylo, xlo+0.1, yhi,"brNDC")
    pt_CMS.SetFillStyle(0)
    pt_CMS.SetBorderSize(0)
    pt_CMS.SetFillColor(0)
    pt_CMS.SetTextFont(61)
    pt_CMS.SetTextSize(0.05)
    pt_CMS.SetTextAlign(11)
    pt_CMS.AddText("CMS")

    pt_prelim = ROOT.TPaveText(xlo+0.09, ylo, xlo+0.3, yhi,"brNDC")
    pt_prelim.SetFillStyle(0)
    pt_prelim.SetBorderSize(0)
    pt_prelim.SetFillColor(0)
    pt_prelim.SetTextFont(52)
    pt_prelim.SetTextSize(0.05*0.76)
    pt_prelim.SetTextAlign(11)
    pt_prelim.AddText("Preliminary" if data else "Simulation")

    return {"lumi":pt_lumi, "CMS":pt_CMS, "type":pt_prelim}
