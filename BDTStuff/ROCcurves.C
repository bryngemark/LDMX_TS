#include <stdio.h>
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include "TTreeReaderValue.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include "TGraph.h"

//#include "DetDescr/DetectorHeader.h"
////#include "DetDescr/DetectorID.h"
////#include "Biasing/EcalProcessFilter.h"
////#include "DetDescr/EcalHexReadout.h"
////#include "EcalHexReadout.h"
////#include "EventDisplay/DetectorGeometry.h"
////#include "Event/EcalHit.h"
////#include "EcalHit.h"
////#include "Event/EventHeader.h"
////#include "EventHeader.h"
////#include "EcalVetoResult.h"
////#include "Event/EcalVetoResult.h"
////#include "Event/HcalVetoResult.h"
////#include "Event/TrackerVetoResult.h"
////#include "Event/SimTrackerHit.h"
////#include "../ldmx-sw/Recon/include/Recon/Event/EventConstants.h"
////#include "../ldmx-sw/TrigScint/include/TrigScint/Event/TrigScintCluster.h"
//
////../ldmx-sw/Recon/include/Recon/Event/EventConstants.h
//
void ROCcurves(){

//FLoat_t residbv=0;
//Float_t residsv=0;
//Float_t numTrab=0;
//Float_t numTras=0;
//TTree back("back","background");
//back.Branch("residb",&residbv,"residualsB");
//back.Branch("numTrab",&numTrab,"numTracksb")
//TTree sig("sig","signal");
//sig.Branch("resids",&residsv,"residualsS");
//sig.Branch("numTras",&numTras,"numTrackss");
Double_t x[100], y[100];
for(int j=0;j<100;j++){
Float_t alpha=.09999-.002*((Float_t)j);
TFile *myFile=TFile::Open("slacback4.root");//"autorunout33.root");
//myFile->Print();
TTree* Event=(TTree*)(myFile->Get(myFile->GetListOfKeys()->At(0)->GetName()));
//Event->Print();
//cout<<myFile->GetListOfKeys()->At(0)->GetName()<<endl;
Float_t residb=0;
Event->SetBranchAddress("residb",&residb);

Float_t counterB=0;
for(int i=0;i<Event->GetEntries();i++){
	Event->GetEntry(i);
	if(not((residb<.2-alpha and residb>.1+alpha) or (residb>.3+alpha))){
		counterB+=1;
	}
	//if(i>40){continue;}
}
//cout<<"hello"<<endl;
counterB/=(Float_t)(Event->GetEntries());
//cout<<"hello2"<<endl;
myFile->Close();
//cout<<"hello3"<<endl;
TFile *myFile2=TFile::Open("slacsig4.root");//"autorunout33.root");
//myFile2->Print();
//cout<<"hello4"<<endl;
TTree* Event2=(TTree*)(myFile2->Get(myFile2->GetListOfKeys()->At(0)->GetName()));
//Event2->Print();
//cout<<"hello5"<<endl;
Float_t resids=0;
//cout<<"hello6"<<endl;
Event2->SetBranchAddress("resids",&resids);
//cout<<"hello7"<<endl;
Float_t counterS=0;
//cout<<"hello8"<<endl;
for(int i=0;i<Event2->GetEntries();i++){
	Event2->GetEntry(i);
	if(not((resids<.2-alpha and resids>.1+alpha) or (resids>.3+alpha))){
		counterS+=1;
	}
	//if(i>40){continue;}
}
counterS/=(Float_t)(Event2->GetEntries());
myFile2->Close();
x[j]=counterB;
y[j]=counterS;
cout<<x[j]<<endl;
cout<<y[j]<<endl;
//TTreeReader myReader(myFile->GetListOfKeys()->At(0)->GetName(),myFile);
//myReader.Print();
//TTreeReaderValue<Float_t> beamEfraback(myReader,"residb");
//while(myReader.Next()){
//	cout<<beamEfraback<<endl;}
}
TGraph *gr1 = new TGraph(100,y,x);
TCanvas *c1 = new TCanvas("c1");
gr1->Draw();
}
