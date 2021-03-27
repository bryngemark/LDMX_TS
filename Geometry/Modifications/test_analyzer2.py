#!/usr/bin/python                                                                                                                                                                       
from ts_digi_container import *
import ROOT as r

import sys
from optparse import OptionParser


def main(options,args) :

    inFile=str(options.inFile)
    passName=str(options.passName)
    modules = ['trigScintDigisTag', 'trigScintDigisUp', 'trigScintDigisDn']

    ## initialize container
    cont = ts_digi_container(inFile,'LDMX_Events')
    for collection in modules :
        cont.get_digi_collection(collection+'_'+passName)
    
    cont.get_cluster_collection('TriggerPadTaggerClusters_digi')
    cont.get_track_collection('TriggerPadTracks_digi')
    
    ## configuration for pretty root plots
    r.gROOT.ProcessLine(".L tdrstyle.C")
    r.gROOT.ProcessLine("setTDRStyle()")
    ## initialize root histogram
    hist = r.TH1F("test","Title;Photo-electrons;Events",40,0,200)
    hBeamEfrac = r.TH1F("hBeamEfrac","beam fraction histo;Fraction of energy deposited by beam electrons;Clusters",101,0,1.01)
    hBeamEfracTracks = r.TH1F("hBeamEfracTracks","beam fraction histo;Fraction of energy deposited by beam electrons;Tracks",101,0,1.01)
    
    
    #my OWN root Stuff
    
    inFile =r.TFile.Open(inFile,"READ")
    Tree=inFile.Get("LDMX_Events;1")
    for entryNum in range(0,Tree.GetEntries()): 
        Tree.GetEntry(entryNum)
        print(Tree.TriggerPadTracks_digi[0].centroid_)
        #print(getattr(Tree.TriggerPadTracks_digi,"centroid_"))
    
    ## loop over events
    #helpper = [0 for i in range(cont.tree.numentries)]
    #print(cont.tree.numentries)
    #print(cont.tree.keys())
    
    print(cont.tree['TriggerPadTracks_digi.constituents_'].array())[1]
    
    #print(branch)
    #print(branch.array())
    #for b in branch.baskets():
    #    print(b)
    for i in range(cont.tree.numentries):
        ## get list of pe for every array for event i
        for collection in modules :
            pes=cont.get_data(collection+'_'+passName,'pe',i)
            for pe in pes : 
                hist.Fill(pe)
 
        beamFracC=cont.get_data('TriggerPadTaggerClusters_digi', 'beamEfrac',i)
        holder1=[]
        for frac in beamFracC :
            holder1.append(frac)
            hBeamEfrac.Fill(frac)
        holder2=[]
        beamFracT=cont.get_data('TriggerPadTracks_digi', 'beamEfrac',i)
        for frac in beamFracT : 
            hBeamEfracTracks.Fill(frac)
            helpper[i]+=1
            holder2.append(frac)
        if helpper[i]>10:
            print(i)
            print(min(holder1))
            print(min(holder2))

    helpper2=[sum([(j==i) for j in helpper]) for i in range(0,6)]
    helpper3=[j*(helpper[j]==2) for j in range(0,len(helpper))]
    
    ###print(helpper2)
    
    ##for h in helpper3:
    ##    if h>0:
    ##        print(h)        
            
    #print(hbeamEfrac[h])
    #print(hbeamEfracTracks[h])
    #print(helpper3)
    #f= open("logFile4.txt","a")
    #for n in helpper2:
    #    f.write(str(n)+" ")
    #f.write("\n")
    
    
    #f.write(str(np.sqrt((float(helpper)/75-2)**2))+"\n")
    ####TO BE GENERATED TO EVALUATE CONFIGURATION FITNESS
    
    #f.close()
    
    #plot!
    
    #c1 = r.TCanvas("c1", "hist canvas", 600,  500)
    
    #hist.SetFillColor(2)
    #hist.SetLineColor(4)
    #hist.SetLineStyle(2)
    #gStyle->SetOptStat("emrou");
    #hist.SetTitle("Photoelectrons Emitted Per Event")
    #hist.Draw()
    #r.gStyle.SetOptStat("emrou")
    #gPad.Update();
    #st = hist.FindObject("stats")
    #st.SetOptState("emrou")
    
    #c1.SaveAs( hist.GetName()+".png")
    #hBeamEfrac.SetLineWidth(3)
    #hBeamEfrac.GetYaxis().SetTitle("Entries")
    #hBeamEfrac.Draw()
    
    #hBeamEfracTracks.SetLineWidth(3)
    #hBeamEfracTracks.SetLineColor(7)
    #hBeamEfracTracks.Draw("same")
    
    #leg=r.TLegend(0.2, 0.5, 0.5, 0.9)
    
    #leg.AddEntry(hBeamEfrac, "Tagger clusters", "L")
    
    #leg.AddEntry(hBeamEfracTracks, "Tracks", "L")
    #leg.Draw()
    #c1.SetLogy();
    #c1.SaveAs( hBeamEfrac.GetName()+".png")



if __name__ == "__main__":
#here: add any option flags needed, and then pick them up in "main" above
    parser = OptionParser()
    parser.add_option('-i', '--inFile', dest='inFile', default='test.root', help='input .root file')
    parser.add_option('-p', '--passName', dest='passName', default='sim', help='pass name to use to look up input variables')

    (options, args) = parser.parse_args()

    main(options,args)
