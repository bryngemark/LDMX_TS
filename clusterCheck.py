from ts_digi_container import *
import ROOT as r

## initialize container
cont = ts_digi_container('~whitbeck/raid/LDMX/v2.2.1/four_electron_tracks.root','LDMX_Events')


cont.get_digi_collection('trigScintDigisTag_reco')
cont.get_digi_collection('trigScintDigisUp_reco')
cont.get_digi_collection('trigScintDigisDn_reco')


cont.get_cluster_collection('TriggerPadTaggerClusters_digi')
cont.get_cluster_collection('TriggerPadUpClusters_digi')
cont.get_cluster_collection('TriggerPadDownClusters_digi')
cont.get_track_collection('TriggerPadTracks_digi')

## configuration for pretty root plots
r.gROOT.ProcessLine(".L tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

## initialize root histogram
PeUp = r.TH1F("Nhits","Title;Number of Photo-electrons > 50; Events",10,0,10)
PeTag = r.TH1F("Numhits","Title;Number of Photo-electrons > 50; Events",10,0,10)
PeDn = r.TH1F("Numhit","Title;Number of Photo-electrons > 50; Events",10,0,10)

clusters = r.TH1F("NumClusters","Title;Number of clusters; Events",10,0,10)
clustersUp = r.TH1F("NumClusters1","Title;Number of clusters; Events",10,0,10)
clustersDn = r.TH1F("NumClusters2","Title;Number of clusters; Events",10,0,10)
Tracks = r.TH1F("NumTracks","Title;Number of Tracks; Events",10,0,10)

hist = r.TH2F("Tagger","Tagger;Number of Photo-electrons > 50;Tracks",8,-0.5,7.5,8,-0.5,7.5)
hist2 = r.TH2F("Upstream","Title;Number of Photo-electrons > 50;Tracks",8,-0.5,7.5,8,-0.5,7.5)
hist3 = r.TH2F("Downstream","Tagger;Number of Photo-electrons > 50;Tracks",8,-0.5,7.5,8,-0.5,7.5)

clushist = r.TH2F("TaggerCluster","TaggerCluster;Number of Clusters;Tracks",8,-0.5,7.5,8,-0.5,7.5)
clushist2 = r.TH2F("UpstreamCluster","UpstreamCluster;Number of Clusters;Tracks",8,-0.5,7.5,8,-0.5,7.5)
clushist3 = r.TH2F("DownstreamCluster","TaggerCluster;Number of Clusters;Tracks",8,-0.5,7.5,8,-0.5,7.5)
## loop over events
for i in range(cont.tree.numentries -1):
    ## get list of pe for tagger array for event i
    pesTag=cont.get_data('trigScintDigisTag_reco','pe',i)
    NpeTag = sum(map(lambda x: x> 50, pesTag)) 
    clusterTag = cont.get_data("TriggerPadTaggerClusters_digi","centroid",i)
    PeTag.Fill(NpeTag)
    clusters.Fill(len(clusterTag))
    ## get list of pe for upstream array for event i
    pesUp = cont.get_data('trigScintDigisUp_reco','pe',i)
    clusterUp = cont.get_data("TriggerPadUpClusters_digi","centroid",i)
    NpeUp = sum(map(lambda x: x> 50, pesUp)) 
    PeUp.Fill(NpeUp)
    clustersUp.Fill(len(clusterUp))
    ## get list of pe for downstream array for event i
    pesDn = cont.get_data('trigScintDigisDn_reco','pe',i)
    clusterDn = cont.get_data("TriggerPadDownClusters_digi","centroid",i)
    NpeDn = sum(map(lambda x: x> 50, pesDn))     
    PeDn.Fill(NpeDn)
    clustersDn.Fill(len(clusterDn))
    
    TrackCentroid = cont.get_data('TriggerPadTracks_digi', 'centroid',i)
    Tracks.Fill(len(TrackCentroid))
    
    hist.Fill(NpeTag,len(TrackCentroid))
    hist2.Fill(NpeUp,len(TrackCentroid))
    hist3.Fill(NpeDn,len(TrackCentroid))

    clushist.Fill(len(clusterTag),len(TrackCentroid))
    clushist2.Fill(len(clusterUp),len(TrackCentroid))
    clushist3.Fill(len(clusterDn),len(TrackCentroid))
# number of hits greater than threshold 50
# number of clusters in various array
# histogram that shows the numner of tracks for each event
c1 = r.TCanvas("c1", "hist canvas", 600,  500)


PeUp.SetLineWidth(3)
PeUp.SetLineColor(2)
PeUp.SetLineStyle(1)
PeUp.Draw()

PeTag.SetLineWidth(3)
PeTag.SetLineColor(1)
PeTag.SetLineStyle(3)
PeTag.Draw("same")


PeDn.SetLineWidth(3)
PeDn.SetLineColor(4)
PeDn.SetLineStyle(2)
PeDn.Draw("same")

leg=r.TLegend(0.2, 0.6, 0.4, 0.9)
leg.AddEntry(PeTag, "tagger", "L")
leg.AddEntry(PeUp, "upstream", "L")
leg.AddEntry(PeDn, "downstream", "L")
leg.Draw()
c1.SaveAs(PeTag.GetName()+".png")

clustersUp.SetLineWidth(3)
clustersUp.SetLineColor(2)
clustersUp.SetLineStyle(1)
clustersUp.Draw()

clusters.SetLineWidth(3)
clusters.SetLineColor(1)
clusters.SetLineStyle(3)
clusters.Draw("same")

clustersDn.SetLineWidth(3)
clustersDn.SetLineColor(4)
clustersDn.SetLineStyle(2)
clustersDn.Draw("same")

leg=r.TLegend(0.6, 0.6, 0.8, 0.9)
leg.AddEntry(clusters, "tagger", "L")
leg.AddEntry(clustersUp, "upstream", "L")
leg.AddEntry(clustersDn, "downstream", "L")
leg.Draw()
c1.SaveAs(clusters.GetName()+".png")

Tracks.SetLineWidth(3)
#Tracks.SetLineColor(2)
Tracks.SetFillColor(4)
Tracks.Draw()
c1.SaveAs(Tracks.GetName()+".png")
c1.SetRightMargin(0.15)

hist.SetTitle("Tagger")
hist.Draw("colz,text")
c1.SaveAs(hist.GetName()+".png")

hist2.Draw("colz,text")
c1.SaveAs(hist2.GetName()+".png")

hist3.Draw("colz,text")
c1.SaveAs(hist3.GetName()+".png")


clushist.Draw("colz,text")
c1.SaveAs(clushist.GetName()+".png")


clushist2.Draw("colz,text")
c1.SaveAs(clushist2.GetName()+".png")

clushist3.Draw("colz,text")
c1.SaveAs(clushist3.GetName()+".png")
