#!/usr/bin/bash 
#SBATCH --partition=bgmp        ### Partition 
#SBATCH --job-name=dedup         ### Job Name 
#SBATCH --output=dedupy%j    ### File in which to store job output  
#SBATCH --time=10:00:00       
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=8 
#SBATCH --account=bgmp 

module load samtools 
 
samtools sort C1_SE_uniqAlign.sam -o C1_SE_uniqAlign.sorted.sam 

#conda activate bgmp_py39

/usr/bin/time -v ./cheney_deduper.py \
-f C1_SE_uniqAlign.sorted.sam \
-u STL96.txt \
-o C1_SE_uniqAlign_deduped.sam

wc -l C1_SE_uniqAlign.sorted.sam
wc -l C1_SE_uniqAlign_deduped.sam

