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
void 2DCutEllipse(){

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
TFile *myFile=TFile::Open("slacback4.root");//"autorunout33.root");
//myFile->Print();
TTree* Event=(TTree*)(myFile->Get(myFile->GetListOfKeys()->At(0)->GetName()));
//Event->Print();
//cout<<myFile->GetListOfKeys()->At(0)->GetName()<<endl;
Float_t residb=0;
Float_t uClb=0;
Event->SetBranchAddress("residb",&residb);
Event->SetBranchAddress("upCl",&uClb);
Float_t counterB=0;
for(int i=0;i<Event->GetEntries();i++){
	Event->GetEntry(i);
	bool T1=((residb<.35)and(residb>0)and(.00068<uClb)and(uClb<.001))or((residb<.35)and(residb>0)and(.00068<uClb)and(uClb<.001));
	bool T2=((residb-.0607)*(residb-.0607)*132.1786+(uClb+.00329)*(uClb+.00329)*57507.95)<1;
	bool T3=((residb-.23357)*(residb-.23357)*224.775+(uClb+.00382)*(uClb+.00382)*57507.95)<1;
	if(T1 or T2 or T3){
		counterB+=1;
	}
}	//if(i>40){continue;}
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
Float_t uCls=0;
//cout<<"hello6"<<endl;
Event2->SetBranchAddress("resids",&resids);
Event2->SetBranchAddress("upCl",&uCls);
//cout<<"hello7"<<endl;
Float_t counterS=0;
//cout<<"hello8"<<endl;
for(int i=0;i<Event2->GetEntries();i++){
	Event2->GetEntry(i);
	bool T1=((resids<.35)and(resids>0)and(.00068<uCls)and(uCls<.001))or((resids<.35)and(resids>0)and(.00068<uCls)and(uCls<.001));
	bool T2=((resids-.0607)*(resids-.0607)*132.1786+(uCls+.00329)*(uCls+.00329)*57507.95)<1;
	bool T3=((resids-.23357)*(resids-.23357)*224.775+(uCls+.00382)*(uCls+.00382)*57507.95)<1;
	if(T1 or T2 or T3){
		counterS+=1;
	}
	//if(i>40){continue;}
}
counterS/=(Float_t)(Event2->GetEntries());
myFile2->Close();
cout<<counterB<<endl;
cout<<counterS<<endl;
//TTreeReader myReader(myFile->GetListOfKeys()->At(0)->GetName(),myFile);
//myReader.Print();
//TTreeReaderValue<Float_t> beamEfraback(myReader,"residb");
//while(myReader.Next()){
//	cout<<beamEfraback<<endl;}
}
