#!/bin/bash
#SBATCH --time=8:00:00
#SBATCH --job-name="Slurm Simple Test Job"
#SBATCH --error="my_job.err"
#SBATCH --output="my_job.output"
python main.py --dataset=Steam --train_dir=default
