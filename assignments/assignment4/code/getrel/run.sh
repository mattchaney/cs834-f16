#!/usr/bin/bash
python q84.py -q $1 && Rscript urpg.R $1 && ./clean.sh
