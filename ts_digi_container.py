import numpy as np
import uproot

## helper function for printing colored text
def colored_format(x,color_id):
    colors=["\033[31m{0}\033[00m", #red
            "\033[32m{0}\033[00m", #green
            "\033[34m{0}\033[00m", #blue
            "\033[35m{0}\033[00m", #purple
            "\033[95m{0}\033[00m", #pink
            "\033[37m{0}\033[00m"  #light gray
            ]
    return colors[color_id].format(x)

class ts_digi_container:
    def __init__(self,file_name='',tree_name=''):
        self.tree = uproot.open(file_name)[tree_name]
        self.digi_dm=["amplitude",
                      "energy",
                      "time",
                      "isNoise",
                      "pe",
                      "xpos","ypos","zpos",
                      "barID",
                      "beamEfrac"]

        self.cluster_dm=["energy",
                         "time",
                         "centroid",
                         "PE",
                         "seed",
                         "nHits",
                         "hitIDs",
                         "beamEfrac"]

        self.track_dm=[  "centroid",
                         "residual",
                         "nClusters",
                         "beamEfrac"]

        self.data={}
        self.event_data={}
        self.cache={}
        self.NUM_CELLS=50
    
    ## helper function for formatting branch names
    ## generally users won't use this...
    def extend_branch_names(self,coll,branch_list):
        new_list=[]
        for branch in branch_list:
            new_list.append(coll+'.'+branch+'_')
        return new_list

    ## Dump an ascii event display and some truth level information
    ## for a list of events. 
    def dump(self,events,coll_name='trigScintDigis'):

        print( 'legend: RED noise/secondaries' )
        print( '        PINK mixed secondaries and beam electrons' )
        print( '        BLUE beam electrons' )

        for event in events: 
            format_row=" {:>2} "*self.NUM_CELLS
            truth_barID=['o']*self.NUM_CELLS
            for e in self.get_truth_y(event):
                if e >= 0 and e < self.NUM_CELLS :
                    truth_barID[int(e)]='x'
            print( ' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ' )
            print( ' event:',event )
            print( ' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ' )
            print( 'true number of electrons:',self.get_num_beam_electrons(event) )
            print( 'ecal energy:',self.get_ecal_energy(event) )
            print( format_row.format(*truth_barID) )
            data = [self.print_array(coll_name+'Tag_sim',event),
                    self.print_array(coll_name+'Dn_sim',event),
                    self.print_array(coll_name+'Up_sim',event)]
            for row in data : 
                print( format_row.format(*row) )
            print( ' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ' )

    ## Extract information for a given array to be printed
    ## NOTE** this function doesn't explicitly print anything **
    def print_array(self,coll,event):
        pes=self.get_data(coll,'pe',event)
        ids=self.get_data(coll,'barID',event)
        beamFrac=self.get_data(coll,'beamEfrac',event)
        channels=['0']*self.NUM_CELLS
        for i in zip(pes,ids,beamFrac):
            if i[1] > 49 : 
                print( "error: id is greater than NUM_CELLS:",i[1] )
                continue
            if i[2] < 0.001 : 
                channels[i[1]]=colored_format(str(int(i[0])),0)
            elif i[2] < 1. : 
                channels[i[1]]=colored_format(str(int(i[0])),4)
            else : 
                channels[i[1]]=colored_format(str(int(i[0])),2)
        return channels

    ## Get total energy as measured in the ecal
    ## this simply sums sim hits and doesn't include reconstruction efects
    def get_ecal_energy(self,event=-1,coll_name='EcalSimHits_sim'):
        self.data.update(self.tree.arrays([coll_name+'.edep_']),cache=self.cache)
        self.data['ecal_total_energy']=map(np.sum,self.data[coll_name+'.edep_'])
        if event<0 :
            return self.data['ecal_total_energy']
        if event>=self.tree.numentries :
            return None
        return self.data['ecal_total_energy'][event]

    
    ## Get the true number of beam electrons
    def get_num_beam_electrons(self,event=-1,coll_name='SimParticles_sim'):
        self.data.update(self.tree.arrays([coll_name+'.first',coll_name+'.second.genStatus_',coll_name+'.second.pdgID_'],cache=self.cache))
        if not 'beam_electron' in self.data:
            self.data['beam_electron'] = (self.data[coll_name+'.second.genStatus_']==1)*(self.data[coll_name+'.second.pdgID_']==11)
            self.data['num_beam_electrons']= map(np.count_nonzero,self.data['beam_electron'])
        if event<0 : 
            return self.data['num_beam_electrons']
        if event>=self.tree.numentries : 
            return None
        return self.data['num_beam_electrons'][event]
    
    ## Get y vertex values for each gen-level electron
    ## position is returned in units of barID
    def get_truth_y(self,event=-1,coll_name='SimParticles_sim'):
        #SimParticles_sim.second.y_
        if not coll_name+'.second.y_' in self.data:
            self.data.update(self.tree.arrays([coll_name+'.second.genStatus_',coll_name+'.second.pdgID_',coll_name+'.second.y_'],cache=self.cache))
            self.data['beam_electron'] = (self.data[coll_name+'.second.genStatus_']==1)*(self.data[coll_name+'.second.pdgID_']==11)
        self.data['beam_ypos']=self.data[coll_name+'.second.y_'][self.data['beam_electron']]
        self.data['beam_barID']=np.divide(np.subtract(self.data[coll_name+'.second.y_'][self.data['beam_electron']],-39.6),1.65)
        if event<0 : 
            return self.data['beam_barID']
        if event>=self.tree.numentries :
            return None
        return self.data['beam_barID'][event]

    ## Load TS digi collection into local memory
    ## NOTE: the list of data members that are loaded 
    ## is configured in self.digi_dm
    def get_digi_collection(self,coll):    
        self.data.update(self.tree.arrays(self.extend_branch_names(coll,self.digi_dm),cache=self.cache))


    ## Load TS cluster collection into local memory
    ## NOTE: the list of data members that are loaded 
    ## is configured in self.cluster_dm
    def get_cluster_collection(self,coll):    
        self.data.update(self.tree.arrays(self.extend_branch_names(coll,self.cluster_dm),cache=self.cache))

        
    ## Load TS track collection into local memory
    ## NOTE: the list of data members that are loaded 
    ## is configured in self.track_dm
    def get_track_collection(self,coll):    
        self.data.update(self.tree.arrays(self.extend_branch_names(coll,self.track_dm),cache=self.cache))

        
    ## get an arbitrary branch from the tree
    ## user should pass the collection and the data member separately
    ## ------- uses:
    ##         get_data('EcalSimHits_sim','edep') # get edep for all events and all sim hits
    ##         get_data('EcalSimHits_sim','edep',10) # get edep for the 11th event and all sim hits
    def get_data(self,coll,data_member,event=-1):
        if event<0 : 
            return self.data[coll+'.'+data_member+'_']
        if event>=self.tree.numentries : 
            return None
        else : 
            return self.data[coll+'.'+data_member+'_'][event]

    ## Computes the number of hits over threshold in a given array (coll)
    ## ------- uses:
    ##         count_hits('trigScintDigisTag_sim',50) # return number of hits for all events
    ##         count_hits('trigScintDigisTag_sim',50,10) # return number of hits for the 10th event
    def count_hits(self,coll,threshold,event=-1):
        pes = self.get_data(coll,'pe',event)
        if pes is None : return None
        if event>=0 : return np.count_nonzero(pes>threshold)
        else : return map(np.count_nonzero,pes>threshold)

    ## Not yet implemented !!!
    def count_clusters(self,coll,threshold,event):
        pes=self.get_data(coll,'pe',event)
        ids=self.get_data(coll,'barID',event)
        print( ids[pes>threshold] )
        print( pes[pes>threshold] )
