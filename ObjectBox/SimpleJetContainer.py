class jets:
    """
    Simple event container for jets
    """
    def __init__(self, ptcut = 25, etacut = 2.5, CSVcut = 0.84, HTminpt = 30):
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

    def reset(self):
        self.jets = []
        self.bjets = []
        self.nJets = 0
        self.nJetsCUT = 0
        self.nJets40 = 0
        self.nCSVM = 0
        self.HT = 0

    def add(self, pt, eta, phi, csv):
        #print "adding jet "+str(self.nJets)+"_",pt, eta, phi, csv
        if pt > self.ptcut and abs(eta) < self.etacut:
            self.jets.append(jet(pt, eta, phi, csv))
            if pt > self.HTminpt:
                self.HT += pt
                self.nJetsCUT += 1
            if pt > 40:
                self.nJets40 += 1
            if csv > self.CSVcut:
                self.bjets.append(jet(pt, eta, phi, csv))
                self.nCSVM += 1
            self.nJets += 1

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
