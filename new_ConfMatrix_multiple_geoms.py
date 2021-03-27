from ts_digi_container import *
import ROOT as r


r.gROOT.ProcessLine(".L tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")
runs_first_geom = ["clustered_ldmx_run5_1e_100R_10000events_yoshebgsim.root","clustered_ldmx_run4_2e_100R_10000events_yoshebgsim.root"]
runs_doublebars = ["clustered_ldmx_run7_doublebars_1e_10000events_v2.root","ldmx_run8_doublebars_run8_2e_10000events.root"]
runs_halfgaps = ["ldmx_run9_geom3_run9_1e_10000events.root", "ldmx_run10_geom3_run10_2e_10000events.root"]
events = []

conf_matrix_first_geom = r.TH2F("clustered_confusion_first_geom","Title;Number of True Electrons;Tracks",4,0.5,4.5,8,-0.5,7.5)
conf_matrix_doublebars = r.TH2F("clustered_confusion_doublebars","Title;Number of True Electrons;Tracks",4,0.5,4.5,8,-0.5,7.5)
conf_matrix_halfgaps = r.TH2F("clustered_confusion_halfgaps","Title;Number of True Electrons;Tracks",4,0.5,4.5,8,-0.5,7.5)
matrices = [conf_matrix_first_geom, conf_matrix_doublebars,conf_matrix_halfgaps]
geoms_runs = [runs_first_geom, runs_doublebars, runs_halfgaps]

for j in range(len(matrices)):
	for n,num in enumerate(geoms_runs[j]):
    		## initialize container
    		cont = ts_digi_container(geoms_runs[j][n],'LDMX_Events')
    		cont.get_track_collection('TriggerPadTracks_digi')
    		n_event = cont.tree.numentries
    		events.append(n_event)
    		## loop over events
    		for i in range(n_event -1):
        		TrackCentroid = cont.get_data('TriggerPadTracks_digi', 'centroid',i)
        		matrices[j].Fill(n+1,len(TrackCentroid))
# number of clusters in various array
#print(events)
for m in range(len(matrices)):
	for y in range(1,matrices[m].GetNbinsY()+1):
    		for x in range(1,matrices[m].GetNbinsX()+1):
        		if (x <= len(events)):
                		matrices[m].SetBinContent(x,y,conf_matrix.GetBinContent(x,y)/events[x-1])
# histograms that shows the numner of tracks for each event
c1 = r.TCanvas("c1", "hist canvas1", 600, 500)
c2 = r.TCanvas("c2", "hist canvas2", 600, 500)
c3 = r.TCanvas("c3", "hist canvas3", 600, 500)

matrices[0].SetLineWidth(3)
matrices[0].SetLineColor(2)
matrices[0].SetLineStyle(1)
matrices[0].Draw("colz,text")
c1.SetRightMargin(0.15)
c1.SaveAs(matrices[0].GetName()+".png")

matrices[1].SetLineWidth(3)
matrices[1].SetLineColor(3)
matrices[1].SetLineStyle(1)
matrices[1].Draw("colz,text")
c2.SetRightMargin(0.15)
c2.SaveAs(matrices[1].GetName()+".png")

matrices[2].SetLineWidth(3)
matrices[2].SetLineColor(4)
matrices[2].SetLineStyle(1)
matrices[2].Draw("colz,text")
c3.SetRightMargin(0.15)
c3.SaveAs(matrices[3].GetName()+".png")
