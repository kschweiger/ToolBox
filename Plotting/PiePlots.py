import ROOT
from array import array

import math

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

def formatForPieChart(yields):
    singleslices = ['ddQCD', 'ttbarOther', 'ttbarPlusCCbar', 'ttbarPlusB', 'ttbarPlus2B',  'ttbarPlusBBbar']
    signalprocesses = ['ttH_hbb' , 'ttH_nonhbb']
    colors =  [ROOT.kGreen+2, ROOT.kRed-7, ROOT.kRed+1, ROOT.kRed-2, ROOT.kRed+2, ROOT.kRed+3]
    smallBKGsum = 0
    SIGNALsum = 0
    for process in yields:
        if process not in singleslices + signalprocesses:
            smallBKGsum += float(yields[process])
        if process in signalprocesses:
            SIGNALsum += float(yields[process])
    yieldsforChart = []
    for sli in singleslices:
        yieldsforChart.append(float(yields[sli]))
    return singleslices+["ttH","minor"], yieldsforChart+[SIGNALsum,smallBKGsum], colors+[ROOT.kBlue, ROOT.kGray]

def getPieChart(processes, yields, colors, cat):
    #Style stuff
    nicenames = ["d.d QCD","t#bar{t}+lf", "t#bar{t}+c#bar{c}", "t#bar{t}+b", "t#bar{t}+2b", "t#bar{t}+b#bar{b}", "ttH", "Other Bkg"]
    niceTitle = {"j7t3" : "7 Jets, 3 b-tags",
                 "j7t4" : "7 Jets, #geq 4 b-tags",
                 "j8t3" : "8 Jets, 3 b-tags",
                 "j8t4" : "8 Jets, #geq 4 b-tags",
                 "j9t3" : "#geq 9 Jets, 3 b-tags",
                 "j9t4" : "#geq 9 Jets, #geq 4 b-tags"}

    chart = ROOT.TPie("Chart_"+cat, "Chart_"+cat, len(processes), array('f', yields))
    chart.SetTitle("#scale[1.6]{"+niceTitle[cat]+"}")
    #print chart.GetTitleOffset()
    #chart.GetTitleSize()
    for iprocess, process in enumerate(processes):
        chart.SetEntryLabel(iprocess,nicenames[iprocess])
        chart.SetEntryFillColor(iprocess, colors[iprocess])
        #chart.SetLabelFormat("%perc") # Use this to show percentage
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

    catorder = ["j7t3", "j8t3", "j9t3", "j7t4", "j8t4", "j9t4"]
    pathtoDatacards = "/Users/korbinianschweiger/Code/data/ttH/datacards/V25_lepVetoloose_systematics/"
    files = {"j7t3":"shapes_group_fh_j7_t3__mem_FH_4w2h1t_p.txt",
             "j7t4":"shapes_group_fh_j7_t4__mem_FH_3w2h2t_p.txt",
             "j8t3":"shapes_group_fh_j8_t3__mem_FH_4w2h1t_p.txt",
             "j8t4":"shapes_group_fh_j8_t4__mem_FH_3w2h2t_p.txt",
             "j9t3":"shapes_group_fh_j9_t3__mem_FH_4w2h1t_p.txt",
             "j9t4":"shapes_group_fh_j9_t4__mem_FH_4w2h2t_p.txt"}

    charts = {}
    leg = None
    SBs = {}
    for key in files:
        yieldsection = getYieldsfromDataCard(pathtoDatacards+files[key])
        processes, yields, colors = formatForPieChart(yieldsection)
        print key,"\n", processes,"\n", yields,"\n"
        charts[key], leg = getPieChart(processes, yields, colors, key)
        SBs[key] = getSoverB(processes, yields)

    c1 = ROOT.TCanvas("c1","c1",1300, 720)

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
        charts[cat].Draw("")
        if printSoverB:
            S, B = SBs[cat]
            SBlabel[cat] = ROOT.TLatex(0.22, 0.845, "S/B = {:5.4f} S/#sqrt{{B}} = {:5.4f}".format(S/B,S/math.sqrt(B)))
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
    cms = ROOT.TLatex( 0.05, 0.94, '#scale[1.4]{CMS} #it{Work in progress}')
    cms.Draw("same")

    leg.SetX1(0.82)
    leg.SetY1(0.2)
    leg.SetX2(0.98)
    leg.SetY2(0.8)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetFillStyle(0)
    leg.Draw("same")


    c1.Update()
    raw_input("")

if __name__ == "__main__":
    main()
