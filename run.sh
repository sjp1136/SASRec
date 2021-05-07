#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --job-name="Slurm Simple Test Job"
#SBATCH --error="my_job.err"
#SBATCH --output="my_job.output"
python2 main2.py --dataset=Steam4 --train_dir=default
