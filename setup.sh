#!/bin/sh

results="results1"
datafile="datahospital"

mkdir $results

for sigma in 0.1 0.2 0.3 0.4 0.5 0.6
do
   for constraint in "am" "lam"
   do
      python3 ParseData.py $datafile $sigma $constraint > $results/$constraint-hyperedges-hospital-period-1h-$sigma.tsv
      echo "$sigma $constraint"
   done
done

cat $results/lam-* > $results/lam-hyperedges-hospital-period-1h-0.0.tsv
cat $results/am-* > $results/am-hyperedges-hospital-period-1h-0.0.tsv
uniq $results/lam-hyperedges-hospital-period-1h-0.0.tsv > $results/lam-hyperedges-hospital-period-1h-0.0-unique.tsv
uniq $results/am-hyperedges-hospital-period-1h-0.0.tsv > $results/am-hyperedges-hospital-period-1h-0.0-unique.tsv