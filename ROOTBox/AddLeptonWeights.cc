#include <array>

#include "TMath.h"

std::array<float,4> getTriggerWeight(TH2F* hSF, float pt, float muonEta);
std::array<float,4> getLeptonWeight(TH2F* hSFID, TH2F* hSFIso, TGraphAsymmErrors* grSF, float pt, float muonEta);

TH2F* getHistoFromFile(const std::string filename, const std::string Histoname);
TGraphAsymmErrors* getTGraphFromFile(const std::string filename, const std::string Histoname);


void AddLeptonWeights(std::string filename = ""){

  std::string basepathtoHistos = ""; //TODO: Set Base path of SF root files!

  //Histograms for Muon trigger ScaleFactors
  TH2F* hMuTriggerRunBF = getHistoFromFile(basepathtoHistos+"EfficienciesAndSF_RunBtoF.root", "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio");
  TH2F* hMuTriggerRunGH = getHistoFromFile(basepathtoHistos+"EfficienciesAndSF_Period4.root", "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio");

  //Histograms for Lepton ScaleFactors
  //Run B-F
  TH2F* hMuIDRunBF = getHistoFromFile(basepathtoHistos+"MuID_EfficienciesAndSF_BCDEF.root", "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio");
  TH2F* hMuIsoRunBF = getHistoFromFile(basepathtoHistos+"MuIso_EfficienciesAndSF_BCDEF.root", "TightISO_TightID_pt_eta/pt_abseta_ratio");
  TGraphAsymmErrors* grMuTrkRunBF = getTGraphFromFile(basepathtoHistos+"fits_BCDEF.root", "ratio_eff_aeta_dr030e030_corr");
  //Run G-H
  TH2F* hMuIDRunGH = getHistoFromFile(basepathtoHistos+"MuID_EfficienciesAndSF_GH.root", "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio");
  TH2F* hMuIsoRunGH = getHistoFromFile(basepathtoHistos+"MuIso_EfficienciesAndSF_GH.root", "TightISO_TightID_pt_eta/pt_abseta_ratio");
  TGraphAsymmErrors* grMuTrkRunGH = getTGraphFromFile(basepathtoHistos+"fits_GH.root", "ratio_eff_aeta_dr030e030_corr");


  if (filename != ""){
    TFile* testfile = TFile::Open( (filename).c_str(), "read" );
    if (testfile == NULL){
      std::cout << "Inputfile is NULL" << std::endl;
      return;
    }
    delete testfile;
  }
  TFile* file = TFile::Open( (filename).c_str(), "update" );

  // load tree
  TTree *tree = (TTree*)file->Get("tree");

  // Declare calculated variables
  int numEvents = 0;
  double jetpt[20];
  double jeteta[20];

  double leppt[10];
  double lepeta[10];
  double lepID[10];

  unsigned int run;

  float TriggerSF_ = 0;
  float TriggerSFerr_ = 0;

  float LeptonSF_ = 0;
  float LeptonSFerr_ = 0;

  // variables to save in new trees
  float MuTriggerWeight;
  float MuTriggerWeighterror;
  float MuTriggerWeightUp;
  float MuTriggerWeightDown;

  float MuWeight;
  float MuWeighterror;
  float MuWeightUp;
  float MuWeightDown;

  TBranch *bTW = tree->Branch("MuTriggerWeight",  &MuTriggerWeight, "MuTriggerWeight/F");
  TBranch *bTWerr = tree->Branch("MuTriggerWeightErr",  &MuTriggerWeighterror, "MuTriggerWeightErr/F");
  TBranch *bTWUp = tree->Branch("MuTriggerWeightUp",  &MuTriggerWeightUp, "MuTriggerWeightUp/F");
  TBranch *bTWDown = tree->Branch("MuTriggerWeightDown",  &MuTriggerWeightDown, "MuTriggerWeightDown/F");

  TBranch *bLW = tree->Branch("MuWeight",  &MuTriggerWeight, "MuWeight/F");
  TBranch *bLWerr = tree->Branch("MuWeightErr",  &MuTriggerWeighterror, "MuWeightErr/F");
  TBranch *bLWUp = tree->Branch("MuWeightUp",  &MuTriggerWeightUp, "MuWeightUp/F");
  TBranch *bLWDown = tree->Branch("MuWeightDown",  &MuTriggerWeightDown, "MuWeightDown/F");
  //tree->Branch("jet_eta",      jet_eta,       "jet_eta[njet]/F");

  // Connect the branches with their member variables.
  if(!tree) return;
  tree->SetBranchAddress("MuTriggerWeight", &MuTriggerWeight);
  tree->SetBranchAddress("MuTriggerWeightErr", &MuTriggerWeighterror);
  tree->SetBranchAddress("MuTriggerWeightUp", &MuTriggerWeightUp);
  tree->SetBranchAddress("MuTriggerWeightDown", &MuTriggerWeightDown);


  tree->SetBranchAddress("MuWeight", &MuWeight);
  tree->SetBranchAddress("MuWeightErr", &MuWeighterror);
  tree->SetBranchAddress("MuWeightUp", &MuWeightUp);
  tree->SetBranchAddress("MuWeightDown", &MuWeightDown);

  tree->SetBranchAddress("jets_pt", &jetpt);
  tree->SetBranchAddress("jets_eta", &jeteta);
  tree->SetBranchAddress("leps_pt", &leppt);
  tree->SetBranchAddress("leps_eta", &lepeta);
  tree->SetBranchAddress("leps_pdgId", &lepID);

  tree->SetBranchAddress("run", &run);


  int totalEntries = tree->GetEntries();

  // start the clock....
  auto t0 = chrono::high_resolution_clock::now();

  cout << "doing " << filename << endl;
  cout << "totalEntries " << totalEntries << endl;
  // loop over events
  for(int entry=0; entry < totalEntries; entry++){
    tree->GetEntry(entry);
    numEvents++;

    std::array<float, 4> Triggerweight = {0.0, 0.0, 0.0, 0.0};
    std::array<float, 4> Leptonweight = {0.0, 0.0, 0.0, 0.0};

    //cout << "Run = " << run << " LepID = " << lepID[0] << " Lep pT = " << leppt[0] << " Let eta = " <<  fabs( lepeta[0] ) << endl;

    if (lepID[0] == 13 || lepID[0] == -13){
      if (run <= 280385){
        Triggerweight = getTriggerWeight(hMuTriggerRunBF, leppt[0], lepeta[0]);
        Leptonweight = getLeptonWeight(hMuIDRunBF, hMuIsoRunBF, grMuTrkRunBF, leppt[0], lepeta[0]);
      }
      else {
        Triggerweight = getTriggerWeight(hMuTriggerRunGH, leppt[0], lepeta[0]);
        Leptonweight = getLeptonWeight(hMuIDRunGH, hMuIsoRunGH, grMuTrkRunGH, leppt[0], lepeta[0]);
      }
    }

    MuTriggerWeight = Triggerweight[0] ;
    MuTriggerWeighterror = Triggerweight[1] ;
    MuTriggerWeightUp = Triggerweight[2];
    MuTriggerWeightDown = Triggerweight[3];

    MuWeight = Leptonweight[0];
    MuWeighterror = Leptonweight[1];
    MuWeightUp = Leptonweight[2];
    MuWeightDown = Leptonweight[3];


    bTW->Fill();
    bTWerr->Fill();
    bTWUp->Fill();
    bTWDown->Fill();

    bLW->Fill();
    bLWerr->Fill();
    bLWUp->Fill();
    bLWDown->Fill();
  }//end loop over events

  //tree->Print();
  tree->Write();
  delete file;

  cout << "numEvents = " << numEvents << endl;

  // clock for timing
  //auto t01 = chrono::high_resolution_clock::now();
  //cout << "took " << chrono::duration_cast<chrono::milliseconds>(t01-t0).count()*0.001 << " seconds" << endl;

  gApplication->Terminate();
}

TH2F* getHistoFromFile(const std::string filename, const std::string Histoname){

  TFile file(filename.c_str(),"READ");

  TH2F* h = 0;
  file.GetObject(Histoname.c_str(),h);

  if (h == 0){ std::cout << "h is 0 in getHistoFromFile";}



  h->SetDirectory(0);
  file.Close();

  return h;
}


TGraphAsymmErrors* getTGraphFromFile(const std::string filename, const std::string Histoname){
  TFile file(filename.c_str(),"READ");

  TGraphAsymmErrors* h = 0;

  file.GetObject(Histoname.c_str(),h);

  if (h == 0){ std::cout << "h is 0 in getTGraphFromFile";}

  file.Close();

  return h;
}


std::array<float,4> getTriggerWeight(TH2F* hSF, float pt, float muonEta){
  float maxval = 499.99;

  float searchEta=fabs( muonEta );
  float searchPt=TMath::Min( pt ,  maxval);
  int thisBin;

  float nomval = 0;
  float error = 0;

  thisBin = hSF->FindBin( searchPt, searchEta );
  nomval=hSF->GetBinContent( thisBin );
  error=hSF->GetBinError( thisBin );

  //cout << "Mu Trigger" << endl;
  //cout << "Nom = " << nomval << " Err = " << error << endl;

  std::array<float, 4> retarray =  {nomval, error, nomval+error, nomval-error};


  return retarray;
}

std::array<float,4> getLeptonWeight(TH2F* hSFID, TH2F* hSFIso, TGraphAsymmErrors* grSF, float pt, float muonEta){
  float maxval = 499.99;

  float searchEta=fabs( muonEta );
  float searchPt=TMath::Min( pt , maxval );

  //cout << "Search Eta = " << searchEta << " search pt = " << searchPt << endl;

  int thisBinID;
  float nomvalID = 0;
  float errorID = 0;

  thisBinID = hSFID->FindBin( searchPt , searchEta  );
  nomvalID = hSFID->GetBinContent( thisBinID );
  errorID = hSFID->GetBinError( thisBinID );

  //cout << "Mu ID" << endl;
  //cout << "Bin = " << thisBinID <<  " Nom = " << nomvalID << " Err = " << errorID << endl;

  int thisBinIso;
  float nomvalIso = 0;
  float errorIso = 0;
  thisBinIso = hSFID->FindBin( searchPt, searchEta  );
  nomvalIso = hSFID->GetBinContent( thisBinIso );
  errorIso = hSFID->GetBinError( thisBinIso );

  //cout << "Mu Iso" << endl;
  //cout << "Nom = " << nomvalIso << " Err = " << errorIso << endl;

  float nomvalTrk = 0;
  float errorTrkHigh = 0;
  float errorTrkLow = 0;
  //Tracking SFs from graph
  double x;
  double y;
  double l;
  double r;
  int point = -1;
  for(int i = 0; i < grSF->GetN(); i++) {
     grSF->GetPoint(i, x, y);

      l = x - grSF->GetErrorXlow(i);
      r = x + grSF->GetErrorXhigh(i);

      if (l <= x && x < r){
        point = i;
        break;
      }
  }
  if (point >= 0){
    double x_;
    double y_;

    grSF->GetPoint(point, x_, y_);
    nomvalTrk = y_;

    errorTrkHigh = grSF->GetErrorYhigh(point);
    errorTrkLow = grSF->GetErrorYlow(point);
  }

  //cout << "Mu Tracking" << endl;
  //cout << "Nom = " << nomvalTrk << " Err = " << errorTrkLow << " | " << errorTrkHigh << endl;

  std::array<float, 4> retarray =  { nomvalID*nomvalIso*nomvalTrk, 0.0 ,
                                    (nomvalID+errorID)*(nomvalIso+errorIso)*(nomvalTrk+errorTrkHigh),
                                    (nomvalID-errorID)*(nomvalIso-errorIso)*(nomvalTrk-errorTrkLow)};

  //cout << "--------------> " << retarray[0] << " " << retarray[2] << endl;

  return retarray;

}
