#!/bin/bash
BIN_DATA="/home/haukurpj/Resources/Data/DIM/DIM_2020.06_SHsnid.csv"
# 3=gen, 4=fl, 6=mark
cut $BIN_DATA -d ";" -f 3,4,6 | sort | uniq > bin_unique_categories.txt
cut bin_unique_categories.txt -d ";" -f 1 | sort | uniq > unique_gen.txt
cut bin_unique_categories.txt -d ";" -f 2 | sort | uniq > unique_fl.txt
cut bin_unique_categories.txt -d ";" -f 3 | sort | uniq > unique_mark.txt