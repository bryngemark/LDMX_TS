#!/usr/bin/python                                                                                                                                                                                      

import sys
import os


# we need the ldmx configuration package to construct the object

from LDMX.Framework import ldmxcfg

# first, we define the process, which must have a name which identifies this processing pass ("pass name").
# it's pretty arbitrary but you will see it in the final collection names.

p=ldmxcfg.Process("digi")

#load the template trigger scintillator clustering and tracking configuration files

from LDMX.TrigScint.trigScint import TrigScintClusterProducer
from LDMX.TrigScint.trigScint import trigScintTrack


#clustering: seeding threshold 
tagSeed = 30. 
upSeed= 30.
downSeed = upSeed
#cluster width (upper limit on nHits/cluster)
tagWidth = 2      # can be up to 3 (default)
#cluster threshold: hits below this PE count are neglected
tagClThr = 5.  # default: 1. here use something >> typical electronics noise, which is 1 (sometimes 2) PE

#tracking: max distance between cluster candidate position and seed cluster position
maxDelta = 1.25

clusteringVerbosity=0
trackingVerbosity=0

#maximum number of events to process  
nEv = 10000


if len(sys.argv) < 1 :
    print("The number of beam electrons has to be specified. Use (positional) argument 1 for it.")
    exit(1)
else :
    nPart=sys.argv[1]   #number of beam electrons to use

    
runNb = nPart # "run number"; for file name uniqueness when there are multiple runs -- uses multiplicity as default


if len(sys.argv) > 2 :  
    inputName=sys.argv[2]  #specify the input name if default is not desired                                                                                             
else:
    inputName="ldmx_upstreamElectron_run%i_%se_%sevents.root" %( runNb, nPart, nEv)
    print("Using input file name: "+inputName)

    
if len(sys.argv) > 3 :
    outputName=sys.argv[3]  #specify the output name if default is not desired
else:
    outputName="clustered_"+inputName
    print("Using output file name: "+outputName)

    
# ------------------- all set; propagate these settings in detail, and run  ---------------


# Define the sequence of event processors to be run

# --- clustering ---
clTag=TrigScintClusterProducer.tagger()
clUp=TrigScintClusterProducer.up()
clDown=TrigScintClusterProducer.down()

clTag.verbosity = clusteringVerbosity
clUp.verbosity = clusteringVerbosity
clDown.verbosity = clusteringVerbosity

# here the seeds etc could also be set
clTag.max_cluster_width = tagWidth
clTag.clustering_threshold = tagClThr
clTag.seed_threshold = tagSeed
clUp.seed_threshold = upSeed
clDown.seed_threshold = downSeed

# --- tracking ---
trigScintTrack.verbosity = trackingVerbosity
trigScintTrack.delta_max = maxDelta


p.maxEvents=nEv
p.sequence = [ clTag, clUp, clDown , trigScintTrack ]

# Provide the list of input files to run on
#p.inputFiles=["~/raid/LDMX/trigger_pad_sim/test.root"]
p.inputFiles=[ inputName ] #"ldmx_sim_events.root"]

# Provide the list of output files to produce, either one to contain 
# the results of all input files or one output file name per input file name
#p.outputFiles=["ldmx_digi_events.root"]
p.outputFiles=[outputName]

# Utility function to interpret and print out the configuration to the screen
print(p)

