#!/bin/bash
# Replace the {{...}} placeholders before submitting.

#SBATCH --job-name={{JOB_NAME}}
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err
#SBATCH --partition={{PARTITION}}
#SBATCH --account={{ACCOUNT}}
#SBATCH --nodes={{NODES}}
#SBATCH --ntasks-per-node={{NTASKS_PER_NODE}}
#SBATCH --cpus-per-task={{CPUS_PER_TASK}}
#SBATCH --mem={{MEMORY}}
#SBATCH --time={{TIME_LIMIT}}
#SBATCH --gres=gpu:{{GPU_COUNT}}

set -euo pipefail

mkdir -p logs
cd {{WORKDIR}}

# Site-specific setup goes here.
{{ENV_SETUP}}

# Prefer srun so resources are charged to the job allocation correctly.
srun {{RUN_COMMAND}}
