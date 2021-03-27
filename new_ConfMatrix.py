from ts_digi_container import *
import ROOT as r


r.gROOT.ProcessLine(".L tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")
E_num = ["one","two","three","four"]
events = [] 

conf_matrix = r.TH2F("Confusion_Matrix","Tittle;Number of True Electrons;Tracks",4,0.5,4.5,8,-0.5,7.5)
for n,num in enumerate(E_num):
    ## initialize container
    cont = ts_digi_container('~whitbeck/raid/LDMX/v2.2.1/'+str(num)+'_electron_tracks.root','LDMX_Events')
    cont.get_track_collection('TriggerPadTracks_digi')
    n_event = cont.tree.numentries
    events.append(n_event)
    ## loop over events
    for i in range(n_event -1):
        TrackCentroid = cont.get_data('TriggerPadTracks_digi', 'centroid',i)
        conf_matrix.Fill(n+1,len(TrackCentroid))
# number of clusters in various array
for x in range(1,conf_matrix.GetNbinsX()+1):
    for y in range(1,conf_matrix.GetNbinsY()+1):
        conf_matrix.SetBinContent(x,y,conf_matrix.GetBinContent(x,y)/events[x-1])
# histogram that shows the numner of tracks for each event
c1 = r.TCanvas("c1", "hist canvas", 600,  500)
conf_matrix.SetLineWidth(3)
conf_matrix.SetLineColor(2)
conf_matrix.SetLineStyle(1)
conf_matrix.Draw("colz,text")
c1.SetRightMargin(0.15)
c1.SaveAs(conf_matrix.GetName()+".png")

