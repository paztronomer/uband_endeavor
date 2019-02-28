#!/bin/bash

echo u-band
nohup submit_widefield.py --paramfile u.param > out_uband_preskysmall_c02.log 2>&1 & 
