#include <array>

void getTriggerWeight(double& ScaleFactor, double& ScaleFactorerror, double HT, double pt, int nB);

void addTriggerWeightToTree(string filename = ""){
  if (filename != ""){
    TFile* testfile = TFile::Open( (filename).c_str(), "read" );
    if (testfile == NULL){
      cout << "Inputfile is NULL" << endl;
      return;
    }
    delete testfile;
  }
  TFile* file = TFile::Open( (filename).c_str(), "update" );

  // load tree
  TTree *tree = (TTree*)file->Get("tree");

  // Declare calculated variables
  int numEvents = 0;
  double HT;
  double pt[20];
  int nBCSVM;

  double SF_ = 0;
  double SFerr_ = 0;

  // variables to save in new trees
  double weightTrigger2;
  double weightTrigger2error;
  double weightTrigger2Up;
  double weightTrigger2Down;

  TBranch *bTW2 = tree->Branch("triggerWeight2",  &weightTrigger2, "triggerWeight2/D");
  TBranch *bTW2err = tree->Branch("triggerWeight2Err",  &weightTrigger2error, "triggerWeight2Err/D");
  TBranch *bTW2Up = tree->Branch("triggerWeight2Up",  &weightTrigger2Up, "triggerWeight2Up/D");
  TBranch *bTW2Down = tree->Branch("triggerWeight2Down",  &weightTrigger2Down, "triggerWeight2Down/D");
  //tree->Branch("jet_eta",      jet_eta,       "jet_eta[njet]/F");

  // Connect the branches with their member variables.
  if(!tree) return;
  tree->SetBranchAddress("triggerWeight2", &weightTrigger2);
  tree->SetBranchAddress("triggerWeight2Err", &weightTrigger2error);
  tree->SetBranchAddress("triggerWeight2Up", &weightTrigger2Up);
  tree->SetBranchAddress("triggerWeight2Down", &weightTrigger2Down);

  tree->SetBranchAddress("ht", &HT);
  tree->SetBranchAddress("jets_pt", &pt);
  tree->SetBranchAddress("nBCSVM", &nBCSVM);

  int totalEntries = tree->GetEntries();

  // start the clock....
  auto t0 = chrono::high_resolution_clock::now();

  cout << "doing " << filename << endl;
  cout << "totalEntries " << totalEntries << endl;
  // loop over events
  for(int entry=0; entry < totalEntries; entry++){
    tree->GetEntry(entry);
    numEvents++;

    SF_ = 0;
    SFerr_ = 0;

    getTriggerWeight(SF_, SFerr_, HT, pt[5], nBCSVM);

    weightTrigger2 = SF_ ;
    weightTrigger2error = SFerr_ ;
    weightTrigger2Up = SF_ + SFerr_ ;
    weightTrigger2Down = SF_ - SFerr_ ;

    if(entry%10000==0 && entry!=0){
      cout << entry << " (" << (100.0*entry/totalEntries) << "%)" << endl;
      cout << "pT=" << pt[5] << " HT=" << HT << " nBCSVM=" << nBCSVM << endl;
      cout << "weight=" << weightTrigger2 << " error=" << weightTrigger2error << endl;
    }

    bTW2->Fill();
    bTW2err->Fill();
    bTW2Up->Fill();
    bTW2Down->Fill();
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

void getTriggerWeight(double& ScaleFactor, double& ScaleFactorerror, double HT, double pt, int nB){
    std::array<double, 10>  pt40;
    std::array<double, 10>  pt45;
    std::array<double, 10>  pt50;
    std::array<double, 10>  pt55;
    std::array<double, 10>  pt60;
    std::array<double, 10>  pt70;
    std::array<double, 10>  pt120;
    // Scale factors
    if (nB <= 1){
       pt40 = {0.8104	,	0.9289	,	0.8780	,	0.9532	,	0.8015	,	0.9071	,	0.8285	,	0.9573	,	1.0000	,	1.000};
       pt45 = {0.8832	,	0.9869	,	0.8729	,	1.0680	,	0.9301	,	0.8944	,	0.9892	,	0.9274	,	1.0000	,	1.000};
       pt50 = {0.7720	,	0.9144	,	0.9215	,	0.9514	,	0.9048	,	0.9316	,	0.8749	,	0.9233	,	1.0000	,	1.000};
       pt55 = {0.8000	,	0.9905	,	0.8356	,	0.9715	,	0.8934	,	0.9817	,	1.0306	,	0.9434	,	1.0000	,	1.000};
       pt60 = {1.0000	,	0.7270	,	0.8643	,	1.0531	,	0.8710	,	0.9373	,	0.9623	,	1.0051	,	1.0000	,	1.000};
       pt70 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	0.9758	,	0.8442	,	0.9935	,	0.9919	,	1.0161	,	1.000};
      pt120 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0667	,	1.000};
    }
     if (nB == 2){
         pt40 = {0.9522	,	0.9632	,	0.9581	,	0.9626	,	0.9533	,	0.9704	,	0.9293	,	0.9476	,	0.9847	,	1.0000};
         pt45 = {0.9611	,	0.9644	,	0.9703	,	0.9796	,	0.9991	,	0.9712	,	0.9636	,	0.9585	,	1.0000	,	1.0000};
         pt50 = {0.9345	,	0.9967	,	1.0002	,	0.9892	,	0.9778	,	0.9974	,	0.9980	,	0.9701	,	1.0000	,	1.0000};
         pt55 = {0.9745	,	0.9900	,	0.9951	,	1.0107	,	0.9797	,	0.9752	,	0.9799	,	0.9787	,	1.0000	,	1.0000};
         pt60 = {0.9482	,	0.9842	,	0.9647	,	0.9991	,	0.9945	,	0.9882	,	0.9913	,	0.9798	,	1.0000	,	1.0000};
         pt70 = {1.0000	,	1.0345	,	0.9883	,	0.9860	,	0.9560	,	0.9869	,	0.9928	,	0.9888	,	0.9948	,	1.0000};
        pt120 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0067	,	1.0000	,	1.0000};
     }
     if (nB == 3){
         pt40 = {0.9718	,	0.9306	,	1.0237	,	0.9924	,	0.9791	,	0.9759	,	0.9877	,	1.0097	,	1.0000	,	1.0000};
         pt45 = {0.9915	,	0.9857	,	0.9844	,	0.9885	,	0.9907	,	0.9932	,	1.0066	,	0.9897	,	1.0000	,	1.0000};
         pt50 = {0.9877	,	1.0153	,	1.0048	,	0.9951	,	0.9906	,	1.0099	,	1.0139	,	0.9753	,	1.0000	,	1.0000};
         pt55 = {0.9449	,	0.9817	,	0.9630	,	0.9874	,	1.0000	,	0.9771	,	0.9849	,	1.0079	,	1.0000	,	1.0000};
         pt60 = {1.0000	,	1.0000	,	0.9946	,	0.9744	,	0.9954	,	0.9884	,	0.9835	,	0.9659	,	1.0000	,	1.0000};
         pt70 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0160	,	1.0049	,	0.9819	,	0.9767	,	1.0000};
        pt120 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
     }
     if (nB >= 4){
         pt40 = {0.9155	,	0.9494	,	1.0408	,	1.0000	,	1.0000	,	0.9643	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
         pt45 = {0.9231	,	1.0000	,	1.0000	,	1.0345	,	1.0000	,	0.9500	,	0.9444	,	0.8333	,	1.0000	,	1.0000};
         pt50 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
         pt55 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	0.9091	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
         pt60 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
         pt70 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0110	,	1.0000	,	1.0000};
        pt120 = {1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000	,	1.0000};
     }
    //Errors
    std::array<double, 10>  pt40err;
    std::array<double, 10>  pt45err;
    std::array<double, 10>  pt50err;
    std::array<double, 10>  pt55err;
    std::array<double, 10>  pt60err;
    std::array<double, 10>  pt70err;
    std::array<double, 10>  pt120err;
    if (nB <= 1){
         pt40err = {0.0555	,	0.0625	,	0.0565	,	0.0608	,	0.0693	,	0.0639	,	0.0591	,	0.0434	,	0.0000	,	0.000};
         pt45err = {0.0731	,	0.0561	,	0.0549	,	0.0614	,	0.0541	,	0.0568	,	0.0547	,	0.0476	,	0.0000	,	0.000};
         pt50err = {0.0991	,	0.0623	,	0.0605	,	0.0649	,	0.0643	,	0.0463	,	0.0509	,	0.0480	,	0.0000	,	0.000};
         pt55err = {0.1176	,	0.0861	,	0.0874	,	0.0799	,	0.0741	,	0.0620	,	0.0333	,	0.0493	,	0.0000	,	0.000};
         pt60err = {0.1000	,	0.1216	,	0.0887	,	0.1212	,	0.0602	,	0.0550	,	0.0355	,	0.0303	,	0.0000	,	0.000};
         pt70err = {0.0000	,	0.1000	,	0.1000	,	0.1000	,	0.0801	,	0.0816	,	0.0341	,	0.0232	,	0.0163	,	0.000};
        pt120err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0689	,	0.000};
     }
    if (nB == 2){
         pt40err = {0.0105	,	0.0099	,	0.0101	,	0.0117	,	0.0133	,	0.0107	,	0.0128	,	0.0139	,	0.0304	,	0.0000};
         pt45err = {0.0113	,	0.0102	,	0.0093	,	0.0102	,	0.0099	,	0.0091	,	0.0107	,	0.0129	,	0.0000	,	0.0000};
         pt50err = {0.0169	,	0.0107	,	0.0076	,	0.0093	,	0.0125	,	0.0082	,	0.0077	,	0.0122	,	0.0000	,	0.0000};
         pt55err = {0.0223	,	0.0145	,	0.0089	,	0.0108	,	0.0126	,	0.0096	,	0.0091	,	0.0110	,	0.0000	,	0.0000};
         pt60err = {0.0494	,	0.0205	,	0.0178	,	0.0106	,	0.0107	,	0.0073	,	0.0064	,	0.0081	,	0.0000	,	0.0000};
         pt70err = {0.0500	,	0.0351	,	0.0311	,	0.0227	,	0.0226	,	0.0105	,	0.0052	,	0.0055	,	0.0078	,	0.0000};
        pt120err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0067	,	0.0000	,	0.0000};
    }
    if (nB == 3){
         pt40err = {0.0199	,	0.0239	,	0.0137	,	0.0173	,	0.0191	,	0.0190	,	0.0178	,	0.0268	,	0.0000	,	0.0000};
         pt45err = {0.0204	,	0.0176	,	0.0137	,	0.0186	,	0.0168	,	0.0191	,	0.0047	,	0.0190	,	0.0000	,	0.0000};
         pt50err = {0.0374	,	0.0089	,	0.0048	,	0.0156	,	0.0162	,	0.0125	,	0.0070	,	0.0224	,	0.0000	,	0.0000};
         pt55err = {0.0522	,	0.0283	,	0.0257	,	0.0203	,	0.0000	,	0.0201	,	0.0172	,	0.0079	,	0.0000	,	0.0000};
         pt60err = {0.0000	,	0.0000	,	0.0305	,	0.0253	,	0.0224	,	0.0140	,	0.0131	,	0.0193	,	0.0000	,	0.0000};
         pt70err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0093	,	0.0035	,	0.0103	,	0.0230	,	0.0000};
        pt120err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
    }
    if (nB >= 4){
         pt40err = {0.0700	,	0.0491	,	0.0294	,	0.0000	,	0.0000	,	0.0351	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
         pt45err = {0.0739	,	0.0000	,	0.0000	,	0.0351	,	0.0000	,	0.0487	,	0.0540	,	0.1521	,	0.0000	,	0.0000};
         pt50err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
         pt55err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0867	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
         pt60err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
         pt70err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0110	,	0.0000	,	0.0000};
        pt120err = {0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000	,	0.0000};
    }

    std::array<double, 7> ptbins = { 40.0, 45.0, 50.0, 55.0, 60.0, 70.0, 120.0 };
    std::array<double, 10> HTbins = { 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 800.0, 1000.0, 1500.0, 2000.0};

    int hBin = -1;
    for (auto& HTbin: HTbins){
      //cout << HT << " " << HTbin << endl;
      if (HT < HTbin) { break; }
      else { hBin++; }
    }

    int pbin = -1;
    for (auto& ptbin: ptbins){
      //cout << pt << " " << ptbin << endl;
      if (pt < ptbin) { break;}
      else { pbin++; }
    }

    if (pbin < 0){ pbin = 0; }
    if (hBin < 0){ hBin = 0; }


    double SF = 1;
    double SFerr = 1;
    //cout << "HT = " << HT << " pT = " << pt << endl;
    //cout << "hBin = " << hBin << " pbin  =" <<  pbin << endl;

    switch(pbin) {
      case 0: SF = pt40[hBin];
              SFerr = pt40err[hBin];
              break;
      case 1: SF = pt45[hBin];
              SFerr = pt45err[hBin];
              break;
      case 2: SF = pt50[hBin];
              SFerr = pt50err[hBin];
              break;
      case 3: SF = pt55[hBin];
              SFerr = pt55err[hBin];
              break;
      case 4: SF = pt60[hBin];
              SFerr = pt60err[hBin];
              break;
      case 5: SF = pt70[hBin];
              SFerr = pt70err[hBin];
              break;
      case 6: SF = pt120[hBin];
              SFerr = pt120err[hBin];
              break;
    }
    //cout << "SF = " << SF << " SFerr  =" <<  SFerr << endl;

    ScaleFactor = SF;
    ScaleFactorerror = SFerr;
}
