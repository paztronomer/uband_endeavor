#!/bin/bash

echo Running a set of RMS values sky_pca. Running over a local copy of binned_fp

nm=Y2N+14_sel4
rms=(0.003 0.004 0.005 0.006 0.007 0.008 0.009 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08)
fplist=bleedmask_binned_fp_sel4.csv

for k in ${rms[@]}
    do 
    
    echo RMS=$k
    echo aux naming "${k/./p}"
    
    sky_pca -i "$fplist" -o pca_"$nm"_u_"${k/./p}"_n04.fits -n 4 --reject_rms $k -s config/u_"$nm"_n04_"${k/./p}".config -l log/u_"$nm"_n0_"${k/./p}".log -v

    done

