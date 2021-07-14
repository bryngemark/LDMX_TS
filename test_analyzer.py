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
    
    cont.get_cluster_collection('TriggerPadTaggerClusters_'+passName)
    cont.get_track_collection('TriggerPadTracks_'+passName)
    
    ## configuration for pretty root plots
    r.gROOT.ProcessLine(".L tdrstyle.C")
    r.gROOT.ProcessLine("setTDRStyle()")
    
    ## initialize root histogram
    hist = r.TH1F("test","Title;Photo-electrons;Events",40,0,200)
    hBeamEfrac = r.TH1F("hBeamEfrac","beam fraction histo;Fraction of energy deposited by beam electrons;Clusters",101,0,1.01)
    hBeamEfracTracks = r.TH1F("hBeamEfracTracks","beam fraction histo;Fraction of energy deposited by beam electrons;Tracks",101,0,1.01)
    
    ## loop over events
    for i in range(cont.tree.numentries):
        ## get list of pe for every array for event i
        for collection in modules :
            pes=cont.get_data(collection+'_'+passName,'pe',i)
            for pe in pes : 
                hist.Fill(pe)
 
        beamFracC=cont.get_data('TriggerPadTaggerClusters_'+passName, 'beamEfrac',i)
        for frac in beamFracC : 
            hBeamEfrac.Fill(frac)
        beamFracT=cont.get_data('TriggerPadTracks_'+passName, 'beamEfrac',i)
        for frac in beamFracT : 
            hBeamEfracTracks.Fill(frac)

    
    #plot!
    c1 = r.TCanvas("c1", "hist canvas", 600,  500)
    hist.SetFillColor(2)
    hist.SetLineColor(4)
    hist.SetLineStyle(2)
    hist.Draw()
    
    c1.SaveAs( hist.GetName()+".png")
    hBeamEfrac.SetLineWidth(3)
    hBeamEfrac.GetYaxis().SetTitle("Entries")
    hBeamEfrac.Draw()
    hBeamEfracTracks.SetLineWidth(3)
    hBeamEfracTracks.SetLineColor(7)
    hBeamEfracTracks.Draw("same")
    
    leg=r.TLegend(0.2, 0.5, 0.5, 0.9)
    leg.AddEntry(hBeamEfrac, "Tagger clusters", "L")
    leg.AddEntry(hBeamEfracTracks, "Tracks", "L")
    leg.Draw()
    c1.SetLogy();
    c1.SaveAs( hBeamEfrac.GetName()+".png")



if __name__ == "__main__":
#here: add any option flags needed, and then pick them up in "main" above
	parser = OptionParser()
	parser.add_option('-i', '--inFile', dest='inFile', default='test.root', help='input .root file')
	parser.add_option('-p', '--passName', dest='passName', default='sim', help='pass name to use to look up input variables')

        (options, args) = parser.parse_args()

        main(options,args)
