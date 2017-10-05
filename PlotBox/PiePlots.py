import ROOT
from array import array

import math

import Helper

def getYieldsfromDataCard(filename):
    #filename = "/Users/korbinianschweiger/Code/data/ttH/datacards/V25_lepVetoloose_systematics/shapes_group_fh_j8_t4__mem_FH_3w2h2t_p.txt"

    yieldsection = None
    with open(filename, 'r') as f:
        read_data = f.read()
        #Get first line of yield section
        isep = 0
        for iline, line in enumerate(read_data.split("\n")):
            if isep == 3:
                break
            if line.startswith("---------------"):
                isep += 1
        yieldsection = read_data.split("\n")[iline:iline+4]
        yieldsection.pop(0) #Pop first line from list
        yieldsection.pop(1) #Pop third line from list
    tmp = {}
    for line in yieldsection:
        l = filter(lambda a: a != "", line.split(" "))
        tmp.update({l[0] : l[1::]})

    yieldsection = {}
    for iprocess in range(len(tmp["process"])):
        yieldsection.update({tmp["process"][iprocess] : tmp["rate"][iprocess]})

    return yieldsection

def getYieldsfromSparseHistos(filename):
    domonitoring = False
    rfile = ROOT.TFile.Open(filename)

    histosforyields = {"j7t3" : [],
                       "j7t4" : [],
                       "j8t3" : [],
                       "j8t4" : [],
                       "j9t3" : [],
                       "j9t4" : []}
    yields = {"j7t3" : {},
              "j7t4" : {},
              "j8t3" : {},
              "j8t4" : {},
              "j9t3" : {},
              "j9t4" : {}}
    catsinHisto = {"fh_j7_t3":"j7t3",
                   "fh_j7_t4":"j7t4",
                   "fh_j8_t3":"j8t3",
                   "fh_j8_t4":"j8t4",
                   "fh_j9_t3":"j9t3",
                   "fh_j9_t4":"j9t4"}
    for key in rfile.GetListOfKeys():
        if len(key.GetName().split("__")) > 3:
            continue
        if key.GetName().split("__")[-1] != "ht":
            continue
        if key.GetName().startswith("qcd"):
            continue
        histosforyields[catsinHisto[key.GetName().split("__")[1]]].append(rfile.Get(key.GetName()))

    #for elem in histosforyields["j7t3"]:
    #    print elem

    for cat in yields:
        for elem in histosforyields[cat]:
            process = elem.GetName().split("__")[0]
            yields[cat][process] = elem.Integral()
    for cat in yields:
        if "ddQCD" not in yields[cat]:
            print "ATTENTION: Calculating ddQCD background in category {0}".format(cat)
            yields[cat]["ddQCD"] = -1
            backgroundyield = 0
            for process in yields[cat]:
                if process not in ["qcd", "data", 'ttH_hbb' , 'ttH_nonhbb']:
                    backgroundyield += yields[cat][process]
            if domonitoring:
                print " ",backgroundyield
                print "  substracting: {0} - {1}".format(yields[cat]["data"], backgroundyield)
            yields[cat]["ddQCD"] = yields[cat]["data"] - backgroundyield
    if domonitoring:
        ttbarsum = 0
        minorsum = 0
        for process in yields["j9t4"]:
            print process,yields["j9t4"][process]
            if process.startswith("ttbar"):
                print "  adding {0} to ttbarsum".format(process)
                ttbarsum += yields["j9t4"][process]
            else:
                if process not in ["ddQCD","qcd", "data", 'ttH_hbb' , 'ttH_nonhbb']:
                    print "  adding {0} to minorsum".format(process)
                    minorsum += yields["j9t4"][process]
        print "ttbarSum",ttbarsum
        print "minorBKG",minorsum
        print "bkgsum",ttbarsum+minorsum
        print "Data (check)",yields["j9t4"]["ddQCD"]+ttbarsum+minorsum
        raw_input("")
    return yields

def formatForPieChart(yields):
    singleslices = ['ddQCD', 'ttbarOther', 'ttbarPlusCCbar', 'ttbarPlusB', 'ttbarPlus2B',  'ttbarPlusBBbar']
    signalprocesses = ['ttH_hbb' , 'ttH_nonhbb']
    danielColors = Helper.colors
    colors = []
    for sl in singleslices:
        colors.append(danielColors[sl])
    #colors =  [ROOT.kGreen+2, ROOT.kRed-7, ROOT.kRed+1, ROOT.kRed-2, ROOT.kRed+2, ROOT.kRed+3]
    smallBKGsum = 0
    SIGNALsum = 0
    for process in yields:
        if process == "data":
            continue
        if process not in singleslices + signalprocesses:
            smallBKGsum += float(yields[process])
        if process in signalprocesses:
            SIGNALsum += float(yields[process])
    yieldsforChart = []
    for sli in singleslices:
        yieldsforChart.append(float(yields[sli]))
    return singleslices+["ttH","minor"], yieldsforChart+[SIGNALsum,smallBKGsum], colors+[danielColors["ttH_hbb"], ROOT.kGray]

def getPieChart(processes, yields, colors, cat):
    #Style stuff
    nicenames = ["ddQCD","t#bar{t}+lf", "t#bar{t}+c#bar{c}", "t#bar{t}+b", "t#bar{t}+2b", "t#bar{t}+b#bar{b}", "t#bar{t}H", "Other Bkg"]
    niceTitle = {"j7t3" : "7 jets, 3 b-tags",
                 "j7t4" : "7 jets, #geq 4 b-tags",
                 "j8t3" : "8 jets, 3 b-tags",
                 "j8t4" : "8 jets, #geq 4 b-tags",
                 "j9t3" : "#geq 9 jets, 3 b-tags",
                 "j9t4" : "#geq 9 jets, #geq 4 b-tags"}

    chart = ROOT.TPie("Chart_"+cat, "Chart_"+cat, len(processes), array('f', yields))
    chart.SetTitle("#scale[1.6]{#bf{"+niceTitle[cat]+"}}")
    #print chart.GetTitleOffset()
    #chart.GetTitleSize()
    for iprocess, process in enumerate(processes):
        chart.SetEntryLabel(iprocess,nicenames[iprocess])
        chart.SetEntryFillColor(iprocess, colors[iprocess])
        #print chart.GetEntryLineWidth(iprocess)
        chart.SetEntryLineWidth(iprocess, 0)
        #chart.SetLabelFormat("%perc") # Use this to show percentage
        #chart.SetLabelFormat("%val")
        chart.SetLabelFormat("")
    leg = chart.MakeLegend()
    chart.SetRadius(chart.GetRadius()*0.8)

    return chart, leg

def getSoverB(processes, yields):
    S = 0
    B = 0
    for iprocess, process in enumerate(processes):
        if process == "ttH":
            S = yields[iprocess]
        else:
            B += yields[iprocess]
    return S, B

def main():
    printSoverB = True
    regions = {"SR" : "Signal Region",
               "VR" : "Validation Region",
               "CR" : "Control Region",
               "CR2" : "Control Region 2"}

    catorder = ["j7t3", "j8t3", "j9t3", "j7t4", "j8t4", "j9t4"]

    charts = {}
    leg = None
    SBs = {}

    plotfromDataCard = False
    plotfromSparse = True
    if plotfromDataCard:
        charts = {"SR" : {}}
        SBs = {"SR" : {}}
        pathtoDatacards = "/Users/korbinianschweiger/Code/data/ttH/datacards/V25_lepVetoloose_systematics/"
        files = {"j7t3":"shapes_group_fh_j7_t3__mem_FH_4w2h1t_p.txt",
                 "j7t4":"shapes_group_fh_j7_t4__mem_FH_3w2h2t_p.txt",
                 "j8t3":"shapes_group_fh_j8_t3__mem_FH_4w2h1t_p.txt",
                 "j8t4":"shapes_group_fh_j8_t4__mem_FH_3w2h2t_p.txt",
                 "j9t3":"shapes_group_fh_j9_t3__mem_FH_4w2h1t_p.txt",
                 "j9t4":"shapes_group_fh_j9_t4__mem_FH_4w2h2t_p.txt"}
        for key in files:
            yieldsection = getYieldsfromDataCard(pathtoDatacards+files[key])
            processes, yields, colors = formatForPieChart(yieldsection)
            #print key,"\n", processes,"\n", yields,"\n"
            charts["SR"][key], leg = getPieChart(processes, yields, colors, key)
            SBs["SR"][key] = getSoverB(processes, yields)


    if plotfromSparse:
        pathtoSparse = "/Users/korbinianschweiger/Code/data/ttH/sparseHistos/V25_lepVetoLoose_systematics_v1_evFix/"
        files = {"CR" : "merged_CR.root",
                 #"VR" : "merged_VR_ddQCD.root",
                 #"CR2" : "merged_CR2.root",
                 "SR" : "merged_SR_ddQCD.root"
                }
        for key in files:
            print "INFO: Making PieCarts for: {0}".format(key)
            charts.update({key : {}})
            SBs.update({key : {}})
            allyields = getYieldsfromSparseHistos(pathtoSparse+files[key])
            for cat in allyields:
                processes, yields, colors = formatForPieChart(allyields[cat])
                #print cat,"\n", processes,"\n", yields,"\n"
                charts[key][cat], leg = getPieChart(processes, yields, colors, cat)
                SBs[key][cat] = getSoverB(processes, yields)

    #print charts
    for key in charts:
        c1 = ROOT.TCanvas("c1"+key,"c1"+key,1300, 720)

        c1.Divide(3,2)
        c1.cd(1).SetPad(0,0.4,0.275,0.9)
        c1.cd(2).SetPad(0.275,0.4,0.55,0.9)
        c1.cd(3).SetPad(0.55,0.4,0.825,0.9)
        c1.cd(4).SetPad(0,-0.075,0.275,0.425)
        c1.cd(5).SetPad(0.275,-0.075,0.55,0.425)
        c1.cd(6).SetPad(0.55,-0.075,0.825,0.425)

        c1.cd(1).SetTopMargin(0.2)
        c1.cd(2).SetTopMargin(0.2)
        c1.cd(3).SetTopMargin(0.2)
        c1.cd(4).SetBottomMargin(0)
        c1.cd(5).SetBottomMargin(0)
        c1.cd(6).SetBottomMargin(0)
        SBlabel = {}

        for icat, cat in enumerate(catorder):
            c1.cd(icat+1)
            #print charts[key][cat]
            charts[key][cat].Draw("")
            if printSoverB:
                S, B = SBs[key][cat]
                SBlabel[cat] = ROOT.TLatex(0.22, 0.8445, "S/B = {:5.4f}, S/#sqrt{{B}} = {:5.4f}".format(S/B,S/math.sqrt(B)))
                SBlabel[cat].Draw("same")

        """
        testchart = ROOT.TPie("a","a",len(processes),array('f', yields))
        #testchart.SortSlices(True)
        for iprocess, process in enumerate(processes):
            testchart.SetEntryLabel(iprocess,process)
            testchart.SetEntryFillColor(iprocess, colors[iprocess])
        testchart.Draw("")
        """
        c1.cd(0)
        cms = ROOT.TLatex( 0.05, 0.94, '#scale[1.4]{#bf{CMS}} #it{Preliminary}')
        cms.SetTextFont(42)
        cms.Draw("same")

        regionlabel = ROOT.TLatex(0.75, 0.94, regions[key])
        regionlabel.SetTextFont(42)
        regionlabel.Draw("same")

        leg.SetX1(0.82)
        leg.SetY1(0.1)
        leg.SetX2(0.98)
        leg.SetY2(0.7)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        leg.Draw("same")


        c1.Update()
        c1.Print("Pie_AllCat_{0}.pdf".format(key))
        raw_input("Charts for {0}. Press ret for next.".format(key))
        c1.Close()

if __name__ == "__main__":

    main()
