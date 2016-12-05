#!/usr/bin/bash
python q84.py -q $1 $2 && Rscript graphs.R $1 $2 && rm -f *.dat
