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

void BDTMakeAndCutNoRead(){

TFile *myFile=TFile::Open("timeFixhalf1and3Sig.root");//"autorunout33.root");
TTree* back=(TTree*)(myFile->Get(myFile->GetListOfKeys()->At(0)->GetName()));
TFile *myFile2=TFile::Open("timeFixhalf1and3Back.root");//"autorunout33.root");
TTree* sign=(TTree*)(myFile2->Get(myFile2->GetListOfKeys()->At(0)->GetName()));
back->Print();
sign->Print();
TFile *outputFile = TFile::Open("TMVANewPoint5.root","recreate");
TMVA::Factory *factory = new TMVA::Factory("TMVAClassification",outputFile);
TMVA::DataLoader *dataloader=new TMVA::DataLoader("dataset");

dataloader->AddVariable("resid",'F');
dataloader->AddVariable("numTra",'I');
dataloader->AddVariable("downCl",'F');
dataloader->AddVariable("upCl",'F');
dataloader->AddVariable("tagCl",'F');
dataloader->AddVariable("dnHits",'F');
dataloader->AddVariable("unHits",'F');
dataloader->AddVariable("tagnHits",'F');


dataloader->AddSignalTree(back,1.0);
dataloader->AddBackgroundTree(sign,1.0);
dataloader->PrepareTrainingAndTestTree("","","nTrain_Signal=0:nTrain_Background=0:SplitMode=Random");
factory->BookMethod(dataloader,TMVA::Types::kBDT,"BDT");
factory->TrainAllMethods();
factory->TestAllMethods();
factory->EvaluateAllMethods();

myFile->Close();
myFile2->Close();
outputFile->Close();

//NOW INCLUDE A READER FOR OTHER EVENTS

}
