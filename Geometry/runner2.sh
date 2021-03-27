#!/bin/bash

#THINGS THAT NEED CHANGING IN THIS ORDER
#filechanger2.py is done

#filechanger3.py is done
#test_analyze2.py is done
#markdowncluster is required to take the varius things markitdown2 copied and make a confusion matrix from them. It will just coppy down the confusion matrix along with which number of electrons its on.



#source ../ldmx-sw/scripts/ldmx-env.sh
source ~/root_install/bin/thisroot.sh;
source ../ldmx-sw/scripts/ldmx-env.sh;
#for i in $(seq 4.1 .1 6.0)
#do
	for j in $(seq .1 .02 .4)
	do
		python filechanger2.py 35 4.5 36 4 37 $j;
		wait $!;
		python filechanger3.py 4.5 $j;
		wait $!;
		#Recmake
		cd ../ldmx-sw/build
		ldmx cmake ..
		wait $!;
		ldmx make install -j2;
		wait $!;
		cd ../../LDMXResearch;
		wait $!;
		for k in $(seq 1 1 4)
		do
			wait $!;
			ldmx fire ../LDMX_TS-master/LDMX_TS-master/runSimAndDigi.py $k 1 autorun;
			wait $!;
			ldmx fire ../LDMX_TS-master/LDMX_TS-master/runClusteringAndTracking.py $k autorun.root autorunout.root;
			wait $!;
			#python markitdown2.py 0 "($i,$j)"	
			#wait $!;
			ldmx python ../LDMX_TS-master/LDMX_TS-master/test_analyzer2.py -i autorunout.root
			wait $!;
			rm ./autorun.root;
			rm ./autorunout.root;
			wait $!;
		done
		wait $!;
	done
#done
