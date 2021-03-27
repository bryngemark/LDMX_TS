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

void BDTMakeAndCut2(){

//NOW INCLUDE A READER FOR OTHER EVENTS

TMVA::Reader *reader = new TMVA::Reader("V:Color:!Silent");
Float_t var[8];

Float_t uservar[8];

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

TFile *myFile3=TFile::Open("FourAll.root");//"autorunout33.root");
//TTreeReader myReader(myFile->GetListOfKeys()->At(0)->GetName(),myFile);
//TTreeReaderArray<Float_t> beamEfrac(myReader,"TriggerPadTracks_sim.beamEfrac_");
//TTreeReaderArray<Float_t> clusterResid(myReader,"TriggerPadTracks_sim.residual_");
TTree* Event=(TTree*)(myFile3->Get(myFile3->GetListOfKeys()->At(0)->GetName()));

//Event->Print();

Event->SetBranchAddress("resid",&uservar[0]);
Event->SetBranchAddress("numTra",&uservar[1]);
Event->SetBranchAddress("downCl",&uservar[2]);
Event->SetBranchAddress("upCl",&uservar[3]);
Event->SetBranchAddress("tagCl",&uservar[4]);
Event->SetBranchAddress("dnHits",&uservar[5]);
Event->SetBranchAddress("unHits",&uservar[6]);
Event->SetBranchAddress("tagnHits",&uservar[7]);
TFile select("./mar18/selectedhalf4.root","recreate");
TTree out("selected","selected");
out.Branch("resid",&outvar[0],"resid");
out.Branch("numTra",&outvar[1],"numTra");
out.Branch("downCl",&outvar[2],"downCl");
out.Branch("upCl",&outvar[3],"upCl");
out.Branch("tagCl",&outvar[4],"tagCl");
out.Branch("dnHits",&outvar[5],"dnHits");
out.Branch("unHits",&outvar[6],"unHits");
out.Branch("tagnHits",&outvar[7],"tagnHits");
out.Branch("BDTscore",&outvar[8],"BDTscore");


//Event->GetEntry(0);
//cout<<uservar[0]<<endl;
//cout<<uservar[1]<<endl;
//cout<<uservar[2]<<endl;

for(int J=0;J<Event->GetEntries();J++){
	Event->GetEntry(J);
	//cout<<J<<endl;
	//cout<<userva[1]<<endl;
	for(int K=0;K<8;K++){
		var[K]=uservar[K];
		outvar[K]=uservar[K];
	}
	outvar[8]=reader->EvaluateMVA("BDT method");
	
	//cout<<uservar[1]<<endl;
	//cout<<var[1]<<endl;
	//cout<<outvar[1]<<endl;
	
	out.Fill();
	//if(reader->EvaluateMVA("BDT method")>0){
	//	out.Fill();
	//}
}

out.Write();
select.Close();
myFile3->Close();

}
