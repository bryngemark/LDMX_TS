from ts_digi_container import *
import ROOT as r

## initialize container
cont = ts_digi_container('/home/whitbeck/raid/LDMX/v2.2.1/one_electron_tracks.root','LDMX_Events')
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

print cont.get_num_beam_electrons(0)

for i in range(100):
    if len(cont.get_data("TriggerPadTracks_digi","centroid",i)) != 1 : 
        cont.dump([i])
        print "tagger clusters"
        for c in cont.get_data("TriggerPadTaggerClusters_digi","centroid",i):
            print c
        print "tagger up"
        for c in cont.get_data("TriggerPadUpClusters_digi","centroid",i):
            print c
        print "tagger down"
        for c in cont.get_data("TriggerPadDownClusters_digi","centroid",i):
            print c
        for t in cont.get_data("TriggerPadTracks_digi","centroid",i):
            print t
        
