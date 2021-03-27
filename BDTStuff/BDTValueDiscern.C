#include <stdio.h>
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include "TTreeReaderValue.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"
#include "TGraph.h"

void BDTValueDiscern(){

//NOW INCLUDE A READER FOR OTHER EVENTS

TMVA::Reader *reader = new TMVA::Reader("V:Color:!Silent");
Float_t var[8];

Float_t uservar[8];

Float_t uservar2[8];

Float_t outvar[9];

reader->AddVariable("resid",&var[0]);
reader->AddVariable("numTra",&var[1]);
reader->AddVariable("downCl",&var[2]);
reader->AddVariable("upCl",&var[3]);
reader->AddVariable("tagCl",&var[4]);
reader->AddVariable("dnHits",&var[5]);
reader->AddVariable("unHits",&var[6]);
reader->AddVariable("tagnHits",&var[7]);
reader->BookMVA("BDT method","dataset/weights/TMVAClassification_BDT.weights.xml");

TFile *myFile3=TFile::Open("timeFixhalf1and3Sig.root");//"autorunout33.root");
TFile *myFile4=TFile::Open("timeFixhalf1and3Back.root");
//TTreeReader myReader(myFile->GetListOfKeys()->At(0)->GetName(),myFile);
//TTreeReaderArray<Float_t> beamEfrac(myReader,"TriggerPadTracks_sim.beamEfrac_");
//TTreeReaderArray<Float_t> clusterResid(myReader,"TriggerPadTracks_sim.residual_");
TTree* Event=(TTree*)(myFile3->Get(myFile3->GetListOfKeys()->At(0)->GetName()));
TTree* Event2=(TTree*)(myFile4->Get(myFile4->GetListOfKeys()->At(0)->GetName()));
//Event->Print();

Event->SetBranchAddress("resid",&uservar[0]);
Event->SetBranchAddress("numTra",&uservar[1]);
Event->SetBranchAddress("downCl",&uservar[2]);
Event->SetBranchAddress("upCl",&uservar[3]);
Event->SetBranchAddress("tagCl",&uservar[4]);
Event->SetBranchAddress("dnHits",&uservar[5]);
Event->SetBranchAddress("unHits",&uservar[6]);
Event->SetBranchAddress("tagnHits",&uservar[7]);

Event2->SetBranchAddress("resid",&uservar2[0]);
Event2->SetBranchAddress("numTra",&uservar2[1]);
Event2->SetBranchAddress("downCl",&uservar2[2]);
Event2->SetBranchAddress("upCl",&uservar2[3]);
Event2->SetBranchAddress("tagCl",&uservar2[4]);
Event2->SetBranchAddress("dnHits",&uservar2[5]);
Event2->SetBranchAddress("unHits",&uservar2[6]);
Event2->SetBranchAddress("tagnHits",&uservar2[7]);


//Event->GetEntry(0);
//cout<<uservar[0]<<endl;
//cout<<uservar[1]<<endl;
//cout<<uservar[2]<<endl;
//for(int H=0;H<40;H++){
//Float_t cutval=-.31+.01*((Float_t)H);
Float_t cutval=.03;
Float_t badrate=0;
for(int J=0;J<Event->GetEntries();J++){
	Event->GetEntry(J);
	//cout<<J<<endl;
	//cout<<userva[1]<<endl;
	for(int K=0;K<8;K++){
		var[K]=uservar[K];
	}
	if(reader->EvaluateMVA("BDT method")<cutval){
		badrate+=1;
	}
}
Float_t badrate2=(Float_t)(Event->GetEntries());
//cout<<badrate<<endl;
//cout<<Event->GetEntries()<<endl;

Float_t goodrate=0;
for(int J=0;J<Event2->GetEntries();J++){
	Event2->GetEntry(J);
	//cout<<J<<endl;
	//cout<<userva[1]<<endl;
	for(int K=0;K<8;K++){
		var[K]=uservar2[K];
	}
	if(reader->EvaluateMVA("BDT method")<cutval){
		goodrate+=1;
	}
}

cout<<cutval<<endl;
Float_t goodrate2=(Float_t)(Event2->GetEntries());
cout<<"BadRate"<<endl;
cout<<(badrate*goodrate2)/(goodrate*badrate2)<<endl;
cout<<"LeftOverGood"<<endl;
cout<<goodrate/goodrate2<<endl;
//}
}
