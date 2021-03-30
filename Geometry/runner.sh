#!/bin/bash

#source ../ldmx-sw/scripts/ldmx-env.sh
source ~/root_install/bin/thisroot.sh
source ../ldmx-sw/scripts/ldmx-env.sh
for i in $(seq 4.1 .1 6.0)
do
	for j in $(seq .1 .02 .4)
	d
		echo "Now on ($ee$j)";
		##################SECTION TO BE RUN OVER WITH VARYING GEOMETRY VALUES
		#Following python file changes the constants.gdml file automatically. Need
		#to look directly at the python file to chose which variables are changed
		#Right now configures only to change the first two
		python filechanger2.py 35 $i 36 4 37 $j; 
		wait $!;
		#Recmake
		cd ../ldmx-sw/build
		ldmx cmake ..
		wait $!;
		ldmx make install -j2
		wait $!;
		cd ..
		cd ..
		cd LDMXResearch
		wait $!;	
		#Now you can run the simulation with changed environment
		ldmx fire ../LDMX_TS-master/LDMX_TS-master/runSimAndDigi.py 2 1 autorun;
		wait $!;
		ldmx fire ../LDMX_TS-master/LDMX_TS-master/runClusteringAndTracking.py 2 autorun.root autorunout.root;
		wait $!;
		python markitdown.py 0 "($i,$j)"	
		wait $!;
		
		#root -b -l <<-EOF
	       	#.L read.C
		#float a=read()
		#TString str ("")
		#str.Form("python markitdown.py 1 %f",a)
		#gSystem->Exec(str)
		#.q
		#EOF
		#wait $!;	
		#python markitdown.py $i $j $helper
		
	
		ldmx python ../LDMX_TS-master/LDMX_TS-master/test_analyzer.py -i autorunout.root
		wait $!;
		rm ./autorun.root;
		cp ./autorunout.root "./runToNight/autorunout-$i-$j.root"
		wait $!;
		rm ./autorunout.root;
		wait $!;
		######THIS FIRST SECTION CREATES THE ROOT FILE. A METRIC FROM THEM USING ROOT OUGHT####TO BE GENERATED TO EVALUATE CONFIGURATION FITNESS
	done
done
