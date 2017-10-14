class jets:
    """
    Simple event container for jets
    """
    def __init__(self, ptcut = 25, etacut = 2.5, CSVcut = 0.84, HTminpt = 30, JetID = "loose"):
        self.ptcut = ptcut
        self.etacut = etacut
        self.CSVcut = CSVcut
        self.HTminpt = HTminpt

        self.jets = []
        self.bjets = []
        self.nJets = 0
        self.nJetsCUT = 0
        self.nJets40 = 0
        self.nCSVM = 0
        self.HT = 0

        if JetID in ["loose", "tight", "tightLepVeto"]:
            self.JetID = JetID
        else:
            self.JetID = None
            print "not supported JetID passes. Using None."
        self.additionalVarsSet = False

    def reset(self):
        self.jets = []
        self.bjets = []
        self.nJets = 0
        self.nJetsCUT = 0
        self.nJets40 = 0
        self.nCSVM = 0
        self.HT = 0

        self.additionalVarsSet = False

    def add(self, pt, eta, phi, csv,
            NHEF = -1, NEmEF = -1, CNHEF = -1, CEmEF = -1,
            CMult = -1, muFrac = -1, NConst = -1):
        #print "adding jet "+str(self.nJets)+"_",pt, eta, phi, csv
        if pt > self.ptcut and abs(eta) < self.etacut:
            currentjet = jet(pt, eta, phi, csv)
            if NHEF != -1 and NEmEF != -1 and CNHEF != -1 and CEmEF != -1 and CMult != -1 and muFrac != -1 and NConst != -1:
                currentjet.setadditionalVars(NHEF, NEmEF, CNHEF, CEmEF, CMult, muFrac, NConst)
                self.additionalVarsSet = True
            if ((self.JetID == "loose" and currentjet.PFJetIDLoose) or
                (self.JetID == "tight" and currentjet.PFJetIDTight) or
                (self.JetID == "tightLepVeto" and currentjet.PFJetIDTightLepVeto) or
                (self.JetID is None) ):
                if pt > self.HTminpt:
                    self.HT += pt
                    self.nJetsCUT += 1
                if pt > 40:
                    self.nJets40 += 1
                if csv > self.CSVcut:
                    self.bjets.append(jet(pt, eta, phi, csv))
                    self.nCSVM += 1
                self.nJets += 1
                self.jets.append(currentjet)


    def HT4Jets(self):
        if self.nJetsCUT >= 4:
            return self.HT
        else:
            return 0

    def Print(self):
        print "============"
        print "nJets: {0}, nJetsCUT: {1}, nCSVM: {2}, HT: {3}".format(self.nJets,self.nJetsCUT,self.nCSVM,self.HT)
        for ij, j in enumerate(self.jets):
            print "Jet {0}: pT: {1} | eta: {2} | csv: {3}".format(ij, j.pt, j.eta, j.csv)
        print "============"

    def getCSVorderd(self, debug = False):
        """
        Get a list of jets ordered by CSV (high->low)
        """
        if debug:
            print "DEBUG: Before sorting"
            for jet in self.jets:
                jet.Print()
        import copy
        retlist = []
        cjets = copy.copy(self.jets)
        while( len(cjets) > 0):
            csvmax = -99
            currentjet = None
            currentjetindex = -10
            #print "while: ",len(cjets)
            for ijet, j in enumerate(cjets):
                if j.csv > csvmax:
                    currentjet = j
                    currentjetindex = ijet
                    csvmax = j.csv
            retlist.append(currentjet)
            #print cjets
            cjets.pop(currentjetindex)
            #print cjets
        if debug:
            print "DEBUG: After sorting"
            for jet in retlist:
                jet.Print()
        return retlist

    def getPTorderd(self):
        """
        Get a list of jets ordered by pT (high->low)
        """
        import copy
        retlist = []
        cjets = copy.copy(self.jets)
        while(len(cjets) > 0):
            ptmax = -99
            currentjet = None
            currentjetindex = -10
            for ijet, j in enumerate(cjets):
                if j.pt > ptmax:
                    currentjet = j
                    currentjetindex = ijet
                    ptmax = j.pt
            retlist.append(currentjet)
            cjets.pop(currentjetindex)
        return retlist

class jet:
    """
    Simple container for a single jet
    """
    def __init__(self, pt, eta, phi, csv):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.csv = csv

        self.addVarsSet = False
        self.neutralHadEFrac = 0
        self.neutralEmEFrac = 0
        self.chargedHadEFrac = 0
        self.chargedEmEFrac = 0
        self.chargedMult = 0
        self.muonFraction = 0
        self.numConstituents = 0

        self.PFJetIDLoose = False
        self.PFJetIDTight = False
        self.PFJetIDTightLepVeto = False

    def setadditionalVars(self, NHEF, NEmEF, CNHEF, CEmEF, CMult, muFrac, NConst):
        self.addVarsSet = True
        self.neutralHadEFrac = NHEF
        self.neutralEmEFrac = NEmEF
        self.chargedHadEFrac = CNHEF
        self.chargedEmEFrac = CEmEF
        self.chargedMult = CMult
        self.muonFraction = muFrac
        self.numConstituents = NConst
        if self.numConstituents > 1 and self.chargedMult > 0 and self.chargedHadEFrac > 0:
            if self.neutralHadEFrac < 0.99 and self.neutralEmEFrac < 0.99 and self.chargedEmEFrac < 0.99:
                self.PFJetIDLoose = True
            if self.neutralHadEFrac < 0.90 and self.neutralEmEFrac < 0.90 and self.chargedEmEFrac < 0.99:
                self.PFJetIDTight = True
                if self.muonFraction < 0.8 and self.chargedEmEFrac < 0.90:
                    self.PFJetIDTightLepVeto =  True

    def Print(self):
        print "Jet pt: {0}, eta: {1}, phi: {2}, csv {3}".format(self.pt, self.eta ,self.phi ,self.csv)




if __name__ == "__main__":
    offlineJets = jets()

    offlineJets.add(100, 1.0, 1.0, 0.7)
    offlineJets.add(80, 1.28118562698, 1.0, 0.9)
    offlineJets.add(84, -0.697551846504, 1.0, 0.88)
    offlineJets.add(61, 1.0, 1.0, 0.3)
    offlineJets.add(35, 1.0, 1.0, 0.45)
    offlineJets.add(25, 1.0, 1.0, 0.6)

    offlineJets.Print()

    print "Jets ordered by CSV value"
    csvorderedjets = offlineJets.getCSVorderd()
    for jet in csvorderedjets:
        jet.Print()
    print "Jets ordered by pT value"
    ptoderedjets = offlineJets.getPTorderd()
    for jet in ptoderedjets:
        jet.Print()

