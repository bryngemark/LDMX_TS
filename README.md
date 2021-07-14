This repo is a beginners guide to quick python-based analysis of LDMX trigger scintillator data. 
The code depends on a few packages: [ROOT](https://root.cern.ch/downloading-root), [uproot](https://github.com/scikit-hep/uproot#jagged-array-performance), [matplotlib](https://matplotlib.org/3.2.1/users/installing.html), and [numpy](https://numpy.org/install/). If you use the `unification` LDMX container, you can access all of these, as well as run `ldmx-sw`, by prepending `ldmx` to all your normal commands. 

To set up the container, run

```bash
source [path-to-ldmx-sw]/ldmx-sw/scripts/ldmx-env.sh -b [path-to-ldmx-sw]
ldmx pull dev unification  
```

(where `-b` is the path to the `ldmx-sw` base dir (defaults to `path-to/scripts/../../`), `dev` is the `repo` (for completeness, these can be `dev` (this is what we want), `local` (for something you built yourself), `pro` (for sample production tags)), and `unification` is the `tag`).


NOTE that `[path-to-ldmx-sw]` should be replaced with any (relative) path to the directory where the `ldmx-sw` directory is located in your setup, or `.` for the present working directory (`pwd`). Run this command **every time** you want to run analysis from a fresh shell.

The code is setup such that `ts_digi_container.py` should be used load the tree and
extract information from the tree. In general, users can use the `get_data`
method to pull data from the tree. This function will get an arbitrary branch from 
the tree user should pass the collection and the data member separately.  Don't include
the '_' that is printed at the end of the branch name when one executes `TTree::Show`.
For example you could run the following to get all ECal sim hits.  

```python
get_data('EcalSimHits_sim','edep') # get edep for all sim hits in all events 
get_data('EcalSimHits_sim','edep',10) # get edep for all sim hits in the 11th event  
```

There are also other helpful function that automate various common calculations.  
In general, functions are written to either pass data from all events, when `event=-1`,
or a single event.  There are some cases where its difficult or impossible to extract 
data for all event simultaneously.  You can distinguish these by checking the defualt
value `event` in the method's definition.

## Running the analysis code with the container

The example script is written in python, and to run it inside the container, just prepend your normal `python` command with `ldmx`:

`ldmx python test_analyzer.py`

The script takes a few optional input arguments; scroll to the bottom of the file to understand them, or run the above command with an additional option `-h` for help.

Remember that the container is a little bit of a universe of its own. When it gets set up, the setup script mounts your working directory on the container behind the scenes -- but it can't see your entire file system. Be mindful of this if you try to run scripts that are on completely different paths; in that case you can "mount" that path on the container (like you would with an external disk like a USB drive) using `ldmx mount /path/where/i/keep/my/data`. Again this needs repeating whenever you're in a fresh shell, after you set up the container. 


## Running event simulation with ldmx-sw

You can produce your own events using the runSimAndDigi.py script.

Run it (after sourcing the env script as indicated above, if you're in a fresh shell) as:

`ldmx fire runSimAndDigi.py [number of electrons per event] [optional: run number] [optional: output file name base]`

The first argument is mandatory.
Inside the script, you can also change the number of events generated, or if you want to use a fix electron multiplicity per event (default and easiest) or if it should be varied according to a Poisson distribution around the number you specified. Be mindful that a large number of events/electron multiplicity both lead to longer simulation time and larger output files. 



## Running clustering and tracking on a simulated file 
`ldmx fire runClusteringAndTracking.py [nElectrons] [input file] [output file]`

Here the number of electrons is not really used for anything but some default naming stuff. So it might get removed. 
You can for example use `test.root`, or the output from `runSimAndDigi.py`, as input file. You might need to change the pass name in  `p=ldmxcfg.Process("digi")` to something else than "digi", if this pass already exists.


### parameters in clustering and tracking
The example python script has a few variables of its own, for convenience, listed in the beginning of the script. This is just so you won't have to change parameters a bunch of places in the code. Here I list the real processor parameter names though (and indicate within parentheses what the convenience variables are called).

#### clustering: can be different for each pad
`seed_threshold` (set for instance by `tagSeed`): cluster seeding threshold, in number of PE

`clustering_threshold` (e.g. `tagClThr`): the minimum number of PE for a hit to even be considered in clustering (so this is a hard cut-off, in addition to the seeding threshold)

`max_cluster_width` (as in `tagWidth`): the cluster width is how many hits in a row can be allowed to form a cluster. Can be set differently for the different pads. 

`output_collection` : this is already set to distinguish tag, up, down, in the predefined function calls. But if several parameter settings are desired in one go, different output collection names should be set.

`verbosity` (`clusteringVerbosity`): in the range from 0 to 3, it makes the clustering algorithm increasingly verbose (where 0 means, very quiet). 


#### tracking: one per track collection
`delta_max` (as in `maxDelta`): the maximum distance (in units of channel number) between the track seeding cluster and the clusters to consider in the other pads

`output_collection` : set a name for the resulting track collection. Useful if you want to run several track producers in one go. Otherwise leave unset; the default is sensible. 

`verbosity` (`trackingVerbosity`): in the range from 0 to 3, it makes the tracking algorithm increasingly verbose (where 0 means, very quiet).


## Simulation files to run over
There is one, very small .root file that ships with this repo: `test.root`, that all example code assumes. It has 100 events, with hits, clusters, and tracks.

A larger sample with sim-level and reco-level TS hits can be found at slac, here:

`/nfs/slac/g/ldmx/users/lene/triggerScint/v2.2.1/`

This is 1M events each, at multiplicities 1,...,4 incoming beam electrons. 


## Running a batch job with a singularity image at SLAC
If you have a singularity image, running jobs with it is pretty easy. Just remember that also here, we need to mount any external directories for them to be accessible by the code inside the image. In this example, a data directory is mounted:

`export dPath="/nfs/slac/g/ldmx/data/mc20/v12/4.0GeV/v2.2.1-2e"`

`bsub -R "select[centos7]" -W 30  singularity run -B ${dPath}:${dPath} /path/to/my-singularity-image.sif . my-ldmx-sw-config.py  "${dPath}/my-infile-name.root" "my-outfile-name.root" `

Here we choose the centos7 machines to avoid SLAC's rhel64 machines which have been acting up in the past (probably not needed with the singularity image though), specify a walltime with `-W [minutes]`, and `-B` is for bind (mount). 

Remember that SLAC batch will happily start writing job output to wherever you're submitting from. So putting all this in a script using some scratch space etc is a nice idea.
