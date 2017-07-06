class jets:
    """
    Simple event container for jets
    """
    def __init__(self):
        self.jets = []
        self.bjets = []
        self.nJets = 0
        self.nJetsCUT = 0
        self.nCSVM = 0
        self.HT = 0

    def reset(self):
        self.jets = []
        self.bjets = []
        self.nJets = 0
        self.nJetsCUT = 0
        self.nCSVM = 0
        self.HT = 0

    def add(self, pt, eta, phi, csv):
        #print "adding jet "+str(self.nJets)+"_",pt, eta, phi, csv
        self.jets.append(jet(pt, eta, phi, csv))
        if pt > 30 and abs(eta) < 2.4:
            self.HT += pt
        if pt > 30 and abs(eta) < 2.4:
            self.nJetsCUT += 1
        if pt > 30 and csv > 0.84 and abs(eta) < 2.4:
            self.bjets.append(jet(pt, eta, phi, csv))
            self.nCSVM += 1
        self.nJets += 1


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
