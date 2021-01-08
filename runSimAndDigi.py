 #!/usr/bin/python


import sys
import os

# we need the ldmx configuration package to construct the object
from LDMX.Framework import ldmxcfg

# first, we define the process, which must have a name which identifies this processing pass ("pass name").
# it's pretty arbitrary but you will see it in the final collection names.
p=ldmxcfg.Process("sim")


from LDMX.SimCore import generators as gen
from LDMX.SimCore import simulator
from LDMX.Biasing import filters
from LDMX.SimCore import simcfg

from LDMX.TrigScint.trigScint import TrigScintDigiProducer

import LDMX.Ecal.EcalGeometry

nEv = 100

if len(sys.argv) < 1 :
    print("The number of beam electrons has to be specified. Use (positional) argument 1 for it.")
    exit(1)
else :
    nPart=sys.argv[1]   #number of beam electrons to use 

    
if len(sys.argv) > 2 :  # "run number"; mostly for guaranteeing uniqueness -- uses multiplicity as default
    runNb=int(sys.argv[2])
else:
    runNb=int(nPart)

if len(sys.argv) > 3 :
    outputName=sys.argv[3]  #specify the output name if default is not desired 
else:
    outputName="ldmx_upstreamElectron"

doPoisson = False #set to true to get poisson varied number of beam electrons instead of fixed


# ------------------- all set; setup in detail, and run with these settings ---------------



mySim = simulator.simulator("mySim")
mySim.runNumber = runNb
mySim.description = "Upstream 4 GeV "+nPart+"-electron beam"
mySim.beamSpotSmear = [20., 80., 0] #mm

# get the path to the installed detector description

from LDMX.Detectors.makePath import *
                                                                      
mySim.setDetector( 'ldmx-det-v12', True  ) #the true should tell it to include scoring planes
mySim.scoringPlanes = makeScoringPlanesPath('ldmx-det-v12')


mpgGen = gen.multi( "mgpGen" ) # this is the line that actually creates the generator
mpgGen.vertex = [ -27.926, 0., -700 ] # mm
mpgGen.nParticles = int(nPart)
mpgGen.pdgID = 11
mpgGen.enablePoisson = doPoisson 

import math
theta = math.radians(4.5)
mpgGen.momentum = [ 4000.*math.sin(theta) , 0, 4000.*math.cos(theta) ] # MeV
#mpgGen.momentum = [ 380., 0., 3981.909 ] #MeV




#set this as the simulator's generator
mySim.generators = [ mpgGen ]

#add simulation to the sequence of stuff the code does 
p.sequence = [ mySim ]

# set the maximum number of events to process

p.maxEvents=nEv


tsDigisUp  =TrigScintDigiProducer.up()
tsDigisTag  =TrigScintDigiProducer.tagger()
tsDigisDown  =TrigScintDigiProducer.down()
tsDigisUp.pe_per_mip = 100.
tsDigisTag.pe_per_mip = tsDigisUp.pe_per_mip
tsDigisDown.pe_per_mip = tsDigisUp.pe_per_mip

# add these to the sequence of processes the code should run
p.sequence=[ mySim, tsDigisUp, tsDigisTag, tsDigisDown ]

#drop scoring plane hits we won't be using anyway
p.keep = [ "drop MagnetScoringPlaneHits", "drop TrackerScoringPlaneHits", "drop HcalScoringPlaneHits"]


# Provide the list of output files to produce
#   When using the simulator to produce events, only one output file is necessary

p.outputFiles=["%s_run%i_%se_%sevents.root" %( outputName, runNb, nPart, nEv) ]


#some logging stuff, helpful to follow what's going on
p.termLogLevel = 1 #include info messages
#print this many events to screen (independent on number of events, except round-off effects when not divisible. so can go up by a factor 2 or so)
logEvents=20
if p.maxEvents < logEvents :
     logEvents = p.maxEvents
p.logFrequency = int( p.maxEvents/logEvents )


# Utility function to interpret and print out the configuration to the screen
print(p)

