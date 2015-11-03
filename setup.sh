#!/bin/sh

NOW=$(date +'%Y-%m-%d-%H-%M-%S')
datafile="rmprox"
results="hyperedge-results/$datafile-$NOW"

mkdir $results
mkdir "$results/lam"
mkdir "$results/am"


for sigma in 0.1 0.2 0.3 0.4 0.5 0.6
do
   for constraint in "am" "lam"
   do
      python3 ParseData.py $datafile $sigma $constraint > $results/$constraint/hyperedges-$sigma.tsv
      echo "$sigma $constraint"
   done
done

cat $results/lam/* > $results/lam/hyperedges-0.0.tsv
cat $results/am/* > $results/am/hyperedges-0.0.tsv
uniq $results/lam/hyperedges-0.0.tsv > $results/lam/hyperedges-0.0-unique.tsv
uniq $results/am/hyperedges-0.0.tsv > $results/am/hyperedges-0.0-unique.tsv

python3 plot.py $results