 #!/usr/bin/python


import sys
import os

# we need the ldmx configuration package to construct the object
from LDMX.Framework import ldmxcfg

# first, we define the process, which must have a name which identifies this processing pass ("pass name").
# it's pretty arbitrary but you will see it in the final collection names.
p=ldmxcfg.Process("digi")

from LDMX.TrigScint.trigScint import TrigScintQIEDigiProducer

import LDMX.Ecal.EcalGeometry                                                                                                                                          
import LDMX.Ecal.ecal_hardcoded_conditions                                                                                                                             

nEv = 100

if len(sys.argv) < 1 :
    print("An input file has to be specified. Use (positional) argument 1 for it.")
    exit(1)
else :
    inputFileName=sys.argv[1]   #input file with sim events to use

    
if len(sys.argv) > 2 :
    outputName=sys.argv[2]  #specify the output name if default is not desired 
else:
    outputName="QIEDigis_"+inputFileName



# ------------------- all set; setup in detail, and run with these settings ---------------


# set the maximum number of events to process

p.maxEvents=nEv


tsDigisUp  =TrigScintQIEDigiProducer.up()
tsDigisTag  =TrigScintQIEDigiProducer.tagger()
tsDigisDown  =TrigScintQIEDigiProducer.down()

# add these to the sequence of processes the code should run
p.sequence=[ tsDigisUp, tsDigisTag, tsDigisDown ]

# Provide the list of output files to produce
p.outputFiles=[ outputName ]


#some logging stuff, helpful to follow what's going on
p.termLogLevel = 1 #include info messages
#print this many events to screen (independent on number of events, except round-off effects when not divisible. so can go up by a factor 2 or so)
logEvents=20
if p.maxEvents < logEvents :
     logEvents = p.maxEvents
p.logFrequency = int( p.maxEvents/logEvents )


# Utility function to interpret and print out the configuration to the screen
print(p)

