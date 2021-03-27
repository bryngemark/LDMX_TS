#include <stdio.h>
#include "TFile.h"
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include <fstream>
#include <iostream>
#include <iomanip>

//#include "DetDescr/DetectorHeader.h"
//#include "DetDescr/DetectorID.h"
//#include "Biasing/EcalProcessFilter.h"
//#include "DetDescr/EcalHexReadout.h"
//#include "EcalHexReadout.h"
//#include "EventDisplay/DetectorGeometry.h"
//#include "Event/EcalHit.h"
//#include "EcalHit.h"
//#include "Event/EventHeader.h"
//#include "EventHeader.h"
//#include "EcalVetoResult.h"
//#include "Event/EcalVetoResult.h"
//#include "Event/HcalVetoResult.h"
//#include "Event/TrackerVetoResult.h"
//#include "Event/SimTrackerHit.h"
//#include "../ldmx-sw/Recon/include/Recon/Event/EventConstants.h"
//#include "../ldmx-sw/TrigScint/include/TrigScint/Event/TrigScintCluster.h"

//../ldmx-sw/Recon/include/Recon/Event/EventConstants.h

float readPurpose2(){
//gSystem.i
//gSystem->Load("../ldmx-sw/build/Event/libEvent.so");
//gSystem->Load("../ldmx-sw/build/DetDescr/libDetDescr.so");
//gSystem->Load("../ldmx-sw/build/TrigScint/libTrigScint.so");
//gROOT->ProcessLine( "gSystem->Load(\"../ldmx-sw/build/Event/libEvent.so\")");
//gROOT->ProcessLine( "gSystem->Load(\"../ldmx-sw/build/Event/libDetDescr.so\")");
//gROOT->ProcessLine( "gSystem->Load(\"../ldmx-sw/build/Event/libTrigScint.so\")");

Float_t residbv=0;
Float_t residsv=0;
Float_t numTrab=0;
Float_t numTras=0;
Float_t downClb=0;
Float_t downCls=0;
Float_t upClb=0;
Float_t upCls=0;
Float_t tagClb=0;
Float_t tagCls=0;

Float_t tagnHits=0;
Float_t tagnHitb=0;
Float_t unHits=0;
Float_t unHitb=0;
Float_t dnHits=0;
Float_t dnHitb=0;

//TFile background("allOfThem.root","recreate");

//TFile background("allOfThem.root","recreate");
TFile background("allOfThem.root","update");
//background.cd();
TTree back("back","background");
back.Branch("resid",&residbv,"resid");
back.Branch("numTra",&numTrab,"numTra");
back.Branch("downCl",&downClb,"downCl");
back.Branch("upCl",&upClb,"upCl");
back.Branch("tagCl",&tagClb,"tagCl");
back.Branch("tagnHits",&tagnHitb,"nHits");
back.Branch("unHits",&unHitb,"unHits");
back.Branch("dnHits",&dnHitb,"dnHits");


ifstream f("namelist.txt");
//string line;
string line;
int CFS=0;
int MoreCount=0;
//NOTE WHEN YOU DO THIS FOR REAL INCLUDE THE FILE LOCATION IN HERE RATHER THAN COPYING IT EVERY TIME IN NAMELIST
while(getline(f, line)){
	cout<<line<<endl;
	string line2 = "/nfs/slac/g/ldmx/data/mc20/v12/4.0GeV/v2.3.0-1e/";
	//string line2 = "/nfs/slac/g/ldmx/data/mc20/v12/4.0GeV/v2.3.0-2e/";
	//string line2 = "/nfs/slac/g/ldmx/data/mc20/v12/4.0GeV/v2.3.0-3e/";
	//string line2 = "/nfs/slac/g/ldmx/data/mc20/v12/4.0GeV/v2.3.0-4e/";
	line2 += line;
	cout<<line2<<endl;
	//char* dest= new char[line2.length()]
	//std::copy(line2.begin(),line2.end(),dest);
	//cout<<dest<<endl;
	//TFile *myFile(line);
	try{
	TFile *myFile=TFile::Open(line2.c_str());//"autorunout33.root");
	
	//TTree *Events=new TTree("","");
	
	TTreeReader myReader(myFile->GetListOfKeys()->At(0)->GetName(),myFile);
	TTreeReaderArray<Float_t> beamEfrac(myReader,"TriggerPadTracks_sim.beamEfrac_");
	TTreeReaderArray<Float_t> clusterResid(myReader,"TriggerPadTracks_sim.residual_");//TriggerPadDownClusters_digi.residuals_");
	TTreeReaderArray<Float_t> downClusT(myReader,"TriggerPadDownClusters_sim.time_");
        TTreeReaderArray<Float_t> upClusT(myReader,"TriggerPadUpClusters_sim.time_");
        TTreeReaderArray<Float_t> tagClusT(myReader,"TriggerPadTaggerClusters_sim.time_");
	
	TTreeReaderArray<Int_t> ntHits(myReader,"TriggerPadTaggerClusters_sim.nHits_");
	TTreeReaderArray<Int_t> ndHits(myReader,"TriggerPadDownClusters_sim.nHits_");
	TTreeReaderArray<Int_t> nuHits(myReader,"TriggerPadUpClusters_sim.nHits_");
	

	//HERE IS WHERE I INSTANTIATE THE SEEDS TO DO IDENTIFICATION STUFF

	TTreeReaderArray<Float_t> trackseed(myReader,"TriggerPadTracks_sim.centroid_");
	TTreeReaderArray<Int_t> downseed(myReader,"TriggerPadDownClusters_sim.seed_");
	TTreeReaderArray<Int_t> tagseed(myReader,"TriggerPadTaggerClusters_sim.seed_");
	TTreeReaderArray<Int_t> upseed(myReader,"TriggerPadUpClusters_sim.seed_");


	//<vector<TrigScintCluster>>
	//TClonesArray * tsclus = new TClonesArray("ldmx::TrigScintCluster");
	//myFile->Close();
	//TTreeReaderArray<vector<TrigScintCluster>> tsclus(myReader,"TriggerPadTracks_digi.constituents_");

	int counter=0;
	//myReader.Print();
	while(myReader.Next()){
		
		//OLD STUFF FOR AVERAGING TIMES	
		
		//Float_t dval=0;
                //Float_t uval=0;
                //Float_t tval=0;
                //for(int i1=0;i1<downClusT.GetSize();i1++){dval+=downClusT[i1];}
                //for(int i2=0;i2<upClusT.GetSize();i2++){uval+=upClusT[i2];}
                //for(int i3=0;i3<tagClusT.GetSize();i3++){tval+=tagClusT[i3];}
		//dval/=downClusT.GetSize();
                //uval/=upClusT.GetSize();
                //tval/=tagClusT.GetSize();
		if(beamEfrac.GetSize()>2){
			MoreCount+=1;
		}
		for(int i=0; i<beamEfrac.GetSize();i++){
			//TIME TO IDNETIFY SEEDS
			int indext=0,indexu=0,indexd=0;
			float mint=100000;
			float helpt=0;
			for(int ii=0;ii<downseed.GetSize();ii++){
				helpt=abs(downseed[ii]-trackseed[i]);
				if(helpt<mint){
					mint=helpt;
					indexd=ii;
				}
			}
			mint=100000;
			for(int jj=0;jj<tagseed.GetSize();jj++){
                                helpt=abs(tagseed[jj]-trackseed[i]);
                                if(helpt<mint){
                                        mint=helpt;
                                        indext=jj;
                                }
                        }
			mint=100000;
			for(int kk=0;kk<upseed.GetSize();kk++){
                                //cout<<"Doing Upseed"<<endl;
				//cout<<kk<<endl;
				helpt=abs(upseed[kk]-trackseed[i]);
                                if(helpt<mint){
                                        mint=helpt;
                                        indexu=kk;
                                }
				//cout<<indexu<<endl;
                        }
			if(true){
				residbv=clusterResid[i];
				numTrab=beamEfrac.GetSize();
				//if((downClb>80) or (upClb>80) or (tagClb>80)){continue;}
				downClb=downClusT[indexd];
                                upClb=upClusT[indexu];
                                tagClb=tagClusT[indext];
				
				if((downClb>50) or (upClb>50) or (tagClb>50)){continue;}
				dnHitb=(Float_t)ndHits[indexd];
                                unHitb=(Float_t)nuHits[indexu];
				tagnHitb=(Float_t)ntHits[indext];
				//cout<<tagnHitb<<endl;
				back.Fill();
				//cout<<"Was Filled"<<endl;
				//cout<<counter<<endl;
			}
			CFS+=1;
			if(CFS%1000==0){
				background.cd();
				back.Write("",TObject::kOverwrite);
				//back.Reset();
				myFile->cd();
			}
		}		
		//cout<<clusterResid[0]<<endl;
		//cout<<tsclus[0].getEnergy()<<endl;

	}
	myFile->Close();
	}catch(...){cout<<"exception";}
	
}

//TFile background("allOfThem.root","recreate");
//back.Write();
background.Close();
cout<<MoreCount<<endl;

//TTree *Events=new TTree();
//myFile.GetObject(myFile.GetListOfKeys()->At(0)->GetName(),Events); 
//Float_t beamFrac;
//Double_t PadDownCluster;
//vector<TrigScintCluster> constit;
//Events->Print();
//Events->SetBranchAddress("TriggerPadTracks_digi.beamEfrac_",&(beamFrac));
//Events->SetBranchAddress("TriggerPadDownClusters_digi.centroid_",&(PadDownCluster));
//Events->SetBranchAddress("TriggerPadTracks_digi.constituents_",&(constit));
//TBranch *BeamFrac=Triggers->GetBranch(Triggers->GetListOfBranches()->At(10)->GetName())
//BeamFrac->SetAddress(&helper);

//Triggers->SetAutoDelete(kTRUE);
//int counter=0;
//while(helper==0){
//Events->GetEntry(counter);
//cout<<helper<<endl;
//cout<<counter<<endl;
//counter+=1;
//}
//
//Long64_t nentries = Events->GetEntries();
//for (Long64_t i =0; i<nentries;i++){
//Events->GetEntry(i);
//if(beamFrac==1){
//cout<<i<<endl;
//cout<<PadDownCluster<<endl;
//cout<<constit.getCentroid()<<endl;
//}	
//if(beamFrac<.75){

//}	

//myFile.GetObject(myFile.GetListOfKeys()->At(0)->GetName(),Events);
//TBranch *Triggers=Events->GetBranch(Events->GetListOfBranches()->At(18)->GetName());
/*TBranch *TriggersCentroid=Triggers->GetBranch(Triggers->GetListOfBranches()->At(0)->GetName())*/
//cout<<Triggers->GetListOfBranches()->At(1)->GetName()<<endl;
//Float_t AA;
//TBranch *TriggersCentroid=Triggers->FindBranch(Triggers->GetListOfBranches()->At(1)->GetName());
//TriggersCentroid->SetBranchAddress("TriggerPadTracks_digi.centroidX_",&AA);
//TLeaf *TriggersCentroidL=TriggersCentroid->FindLeaf(TriggersCentroid->GetListOfLeaves()->At(0)->GetName());
//cout<<TriggersCentroid->GetListOfLeaves()->At(0)->GetName()<<endl;
//TriggersCentroid->GetEntry(0);
//float helper=1;
//helper=AA;
//int counter=0;
//Events->Print();
//while(helper==0){
//TriggersCentroid->Print();
//counter+=1;
//cout<<counter<<endl;
//}
//int helper=TriggersCentroidL->GetMaximumBin();
//float helper=TriggersCentroidL->GetMaximum();
//cout<<helper<<endl;
return 0.0;
/*fp = fopen("./listOfNumbers.txt","w");
fprintf(fp,helper);
fclose(fp);*/
/*TLeaf *TriggersIn=Triggers->GetLeaf(Triggers->GetListOfLeaves()->At(0)->GetName());
cout<<"Got Here"<<endl;
cout<<Events->GetListOfBranches()->At(18)->GetName()<<endl;
cout<<Triggers->GetListOfLeaves()->At(0)->GetName()<<endl;
cout<<TriggersIn->GetLen()<<endl;
TBrowser *T= new TBrowser();
Triggers->Browse(T);
cout<<Triggers->GetBr()<<endl;*/
}
