---
name: lab-cluster-ops
description: Helps connect to lab compute resources and run experiments across SSH hosts, VMs, supercomputers, and Slurm clusters, using Bitwarden Desktop SSH Agent for Bitwarden-managed SSH keys by default. Use whenever the user needs to choose among multiple lab machines, SSH into a server, use a Bitwarden SSH key item, handle SSH plus TOTP, submit or inspect Slurm jobs, sync code, checkpoints, or logs, run training inside tmux, or move an experiment between workstations, VMs, and GPU clusters, even if they only mention a hostname, H100 cluster, HPC, sbatch, squeue, "SSH agent", or "run an experiment".
metadata:
  compatibility: Designed for terminal agents with ssh access. Uses ssh, ssh-agent-compatible sockets such as Bitwarden Desktop SSH Agent, scp or rsync, tmux, git, and Slurm commands when present.
  requires:
    bins: ["ssh"]
---

# Lab Cluster Ops

Use this skill to operate a mixed lab compute environment without re-deriving the workflow every time.

The environment this skill is designed for usually includes:

- several directly maintained SSH servers
- supercomputers that require SSH plus TOTP and use Slurm
- VMs that are fully usable at the guest OS level but not maintained at the physical-host level
- one or more GPU clusters that use SSH and Slurm

## What good execution looks like

Start by reducing ambiguity:

1. Identify the target machine or shortlist.
2. Identify the run mode: inspect, sync, interactive debug, batch job, or artifact collection.
3. Identify the access pattern: plain SSH, SSH plus TOTP, jump host, or Slurm scheduler.
4. Identify the SSH alias and key material that should be used for that machine.
5. Identify the remote workspace and environment bootstrap.

The goal is to leave the user with a working run, a recoverable log location, and a clear next command.

When the user asks to connect, launch, run, submit, sync and start, or keep an experiment alive, treat that as permission to operate the remote system if the agent has shell access and the target is identifiable from the inventory or SSH config. Do the work instead of only writing instructions. Ask a short clarification only when a required login host, account, partition, workspace path, run command, or safety approval is missing.

For long GPU work, a job is not considered started until there is evidence that it survived detachment or scheduler submission. Confirm the session or job after launch, check the log or scheduler state, and report the reattach or monitoring command.

## Preferred sources of truth

Use the most specific source available, in this order:

1. The user's local machine inventory at `~/.config/lab-cluster-ops/machine-inventory.yaml`, when it exists.
2. A machine inventory path the user explicitly provides.
3. The template in [`assets/machine-inventory.template.yaml`](assets/machine-inventory.template.yaml) if they need one.
4. Existing SSH aliases discovered with [`scripts/discover_ssh_hosts.py`](scripts/discover_ssh_hosts.py).
5. A short clarification only when the task is blocked by missing login host, account, partition, or workspace path.

Do not force the user to restate hostnames and auth details if they already exist in `~/.ssh/config`, a prior message, or a machine inventory file.

Do not store real host inventories inside the skill package or source repo. Keep real machine names, login hosts, ports, account references, and Bitwarden item names in the user's config directory, and keep only sanitized templates under `assets/`.

If the user needs a new inventory, copy [`assets/machine-inventory.template.yaml`](assets/machine-inventory.template.yaml) to `~/.config/lab-cluster-ops/machine-inventory.yaml` and fill it there.

## Machine identity and key mapping

Treat per-machine SSH identity as durable configuration, not as an incidental flag passed ad hoc.

For every machine that uses SSH keys, prefer storing these fields in the machine inventory:

- `ssh_alias`: the preferred alias if `~/.ssh/config` already contains the right connection details
- `hostname`, `user`, and `port`: the canonical network coordinates
- `proxyjump`: the jump host alias or explicit jump endpoint when the target is not directly reachable
- `identity_file`: the private key path to use for that machine
- `auth_mode`: for example `ssh-key` or `ssh-key-plus-totp`
- `secret_provider`: for example `bitwarden`
- `bitwarden_item`: the vault item name or id used for passwords, TOTP, or SSH key metadata
- `password_ref`, `totp_ref`, and `ssh_key_ref`: references to secrets, never secret values
- `ssh_key_mode`: use `bitwarden-ssh-agent` for Bitwarden-managed SSH keys
- `identity_agent`: SSH agent socket path to use for that machine, when it differs from the local default

Why this matters:

- labs often expose multiple machines behind the same public hostname but different ports
- different machines may require different private keys
- using the wrong key wastes time and can trigger avoidable auth failures

Prefer connection methods in this order:

1. Bitwarden Desktop SSH Agent when `ssh_key_mode: bitwarden-ssh-agent`
2. `ssh <alias>` when the alias is known-good and already points at the correct key
3. `ssh -i <identity_file> -p <port> <user>@<hostname>` only when a local private-key file is intentionally configured
4. a short clarification only if both alias and key mapping are missing

Do not echo private key contents into chat. Only reference key paths such as `~/.ssh/id_rsa_lab`.

## Bitwarden integration

Use Bitwarden as the preferred local secret provider when the inventory references `secret_provider: bitwarden`.

The inventory should store references, not secret values:

```yaml
secret_provider: bitwarden
bitwarden_item: lab/gpu-host
password_ref: bitwarden:item:lab/gpu-host:password
totp_ref: bitwarden:item:lab/hpc-login:totp
ssh_key_ref: bitwarden:ssh-agent:lab/gpu-host
ssh_key_mode: bitwarden-ssh-agent
identity_agent: ~/.bitwarden-ssh-agent.sock
```

Use Bitwarden CLI for passwords and TOTP:

```bash
bw config server https://vault.bitwarden.com
bw login
export BW_SESSION="$(bw unlock --raw)"
bw sync
bw get password <item-name-or-id>
bw get totp <item-name-or-id>
```

For this lab environment, prefer storing non-secret Bitwarden CLI defaults in a local config file:

```yaml
bitwarden:
  server_url: https://vault.bitwarden.com
  email: <bitwarden-login-email>
```

Then initialize the CLI with:

```bash
bw config server https://vault.bitwarden.com
bw login <bitwarden-login-email>
export BW_SESSION="$(bw unlock --raw)"
```

Use a custom `server_url` only when the lab explicitly uses self-hosted Bitwarden. This email and server URL are configuration, not secrets. Still avoid putting the Bitwarden master password, API key, TOTP seed, or current TOTP codes in any inventory or skill file.

For SSH keys in this lab, use Bitwarden Desktop SSH Agent by default:

- store SSH keys as Bitwarden SSH Key items
- enable SSH Agent in the Bitwarden desktop app
- set `SSH_AUTH_SOCK` or `IdentityAgent` to Bitwarden's SSH agent socket
- use `IdentityFile=none` plus `IdentitiesOnly=no` when an old SSH config alias still points at a stale local key
- verify the expected key comment or fingerprint with `ssh-add -l` before connecting

The macOS Desktop socket used in this environment is:

```bash
~/.bitwarden-ssh-agent.sock
```

Use this pattern for agent-backed machines:

```bash
BW_SSH_AGENT="$HOME/.bitwarden-ssh-agent.sock"
SSH_AUTH_SOCK="$BW_SSH_AGENT" ssh-add -l
ssh \
  -o IdentityAgent="$BW_SSH_AGENT" \
  -o IdentityFile=none \
  -o IdentitiesOnly=no \
  -p <port> <user>@<hostname> '<remote-check-or-command>'
```

If the inventory specifies a jump host, keep the same agent socket and add `ProxyJump`:

```bash
BW_SSH_AGENT="$HOME/.bitwarden-ssh-agent.sock"
ssh \
  -o IdentityAgent="$BW_SSH_AGENT" \
  -o IdentityFile=none \
  -o IdentitiesOnly=no \
  -o ProxyJump=<jump-user>@<jump-hostname>:<jump-port> \
  -p <target-port> <target-user>@<target-hostname> '<remote-check-or-command>'
```

If the local inventory records a `proxyjump_key_ref` and a target `ssh_key_ref`, make sure the agent can serve both keys before connecting. Do not try a direct login path when the local inventory says the target requires a jump host.

The `bw` CLI can unlock and read vault items, passwords, TOTP, and attachments, but it is not the SSH agent. Do not pipe SSH private keys through `bw` or write them to disk unless Bitwarden Desktop SSH Agent is unavailable and the user explicitly accepts the fallback.

Only use attachment-based key sync when the SSH Agent is unavailable or the target workflow explicitly needs a local private-key file. If a key is downloaded from Bitwarden, write it under a restricted directory such as `~/.ssh/lab/` and immediately `chmod 600` it.

The helper [`scripts/bw_lab_secret.py`](scripts/bw_lab_secret.py) wraps common local `bw` calls for this workflow without storing secrets. Use `bw_lab_secret.py configure` to apply the local server URL and email defaults.

## Resource categories

Classify the target before acting:

### 1. Direct SSH server

Use this for self-maintained lab machines that can run long experiments directly.

Prefer:

- `ssh <alias>` for connection
- `ssh -i <identity_file> -p <port> <user>@<hostname>` when a machine-specific key must be enforced explicitly
- `tmux new -As <session>` for long-running work
- `nvidia-smi`, `ps`, `df -h`, and `free -h` for quick health checks

### 2. SSH plus TOTP supercomputer

Use this for school or department HPC systems with a login node and Slurm.

Treat these as two-stage systems:

- authenticate to the login node first
- submit or attach to jobs from the login node
- keep heavy compute off the login node unless the site docs explicitly allow otherwise

When TOTP is required:

- use an interactive terminal or PTY session
- let the user type the one-time code if there is no approved secure automation path
- never ask for the user's TOTP seed
- never write OTP secrets or recovery codes into files or shell history

### 3. VM under your control

Treat the guest OS as directly operable, but do not assume control of the hypervisor, network fabric, or physical host lifecycle.

That means:

- you can connect, install packages inside the guest, and run experiments
- you should not claim you can reboot the host machine, change the VM placement, or fix physical host failures unless the user explicitly says they own that layer

### 4. SSH plus Slurm cluster

Use this for clusters such as a dedicated H100 pool that are accessed over SSH and scheduled with Slurm.

The core pattern is:

- connect to the login or gateway node
- inspect partitions, account, and resource limits
- choose `srun --pty` for short interactive debugging
- choose `sbatch` for normal training runs

### 5. Application-gated direct SSH server

Use this for machines whose hardware is known and useful for planning, but whose login permission is controlled by an application, whitelist, or reservation system.

Treat these as inventory resources, not immediately runnable targets:

- keep their GPU, memory, port, and policy details in the inventory
- check `access_status` before selecting them for a run
- if `access_status` says approval or whitelist is missing, do not try to connect unless the user explicitly asks for an access test
- surface the application constraints when relevant, such as max GPUs per request, reservation window, or process cleanup at permission expiry

## Default workflow

### Step 1: Pick the machine deliberately

Choose based on the user intent:

- quick debugging or one-off commands: the easiest reachable machine with the right data and environment
- long single-node training: direct SSH machine, VM, or cluster node via Slurm
- shared or queue-managed compute: Slurm system
- large GPU jobs or H100-only needs: the H100 cluster
- high-memory A800 workloads: application-gated A800 nodes only after the user has an active approval or reservation

If multiple hosts can work, explain why you chose one.

If a machine is known but currently not accessible, keep it in planning output as "available after approval" instead of pretending it can run immediately.

### Step 2: Reuse existing SSH aliases

Prefer aliases already present in SSH config. If the user does not know the exact alias, run the discovery helper and shortlist likely matches.

If the agent has shell access, the usual discovery command is:

```bash
python scripts/discover_ssh_hosts.py
```

Then reconcile the discovered alias against the machine inventory. If the inventory says a machine uses `ssh_key_mode: bitwarden-ssh-agent`, use the recorded Bitwarden key and `IdentityAgent` even when the SSH alias still has a stale `IdentityFile`. If the inventory says a machine has a dedicated `identity_file`, keep that mapping. Do not silently swap to another alias on the same hostname unless the user has confirmed the aliases are interchangeable.

### Step 3: Decide how to move code and data

Prefer the lightest reliable approach:

- code already in git and remote can pull: use git on the remote
- local worktree needs to be mirrored: use `rsync`
- a few files only: use `scp`
- large datasets already exist on the cluster: reuse them in place instead of copying

When syncing experiment outputs back, prefer preserving structure and timestamps.

### Step 4: Launch and confirm the run

For any long-running GPU command on a direct SSH host or VM:

- prefer `tmux` for persistence
- use `screen` only when `tmux` is unavailable
- write stdout and stderr to a timestamped log under a known directory
- keep the exact launch command recoverable in the session history or a small run script
- after detaching, wait briefly and verify that the session still exists and that the process is active
- check a small slice of logs and GPU/process state before reporting success
- do not use a bare trailing `&` as the primary persistence mechanism for training jobs

For Slurm systems, `sbatch` submission is only the first step. Follow it with `squeue`, `scontrol show job`, or `sacct` depending on whether the job is pending, running, or already finished.

## Run patterns

### Direct SSH or VM run

Use a persistent shell session so the run survives disconnects:

```bash
ssh <alias>
tmux new -As exp-<short-name>
cd <remote-workdir>
<env-bootstrap>
<run-command>
```

If the inventory tracks a machine-specific key and you are not relying on a trusted SSH alias, prefer:

```bash
ssh -i <identity_file> -p <port> <user>@<hostname>
tmux new -As exp-<short-name>
cd <remote-workdir>
<env-bootstrap>
<run-command>
```

For detached execution, prefer creating the session and log explicitly:

```bash
ssh <alias>
cd <remote-workdir>
mkdir -p logs
tmux new-session -d -s exp-<short-name> 'bash -lc "<env-bootstrap> && <run-command> 2>&1 | tee -a logs/<short-name>-$(date +%Y%m%d-%H%M%S).log"'
tmux has-session -t exp-<short-name>
tmux capture-pane -pt exp-<short-name> -S -80
nvidia-smi
```

For complex environment setup or commands with nested quotes, write a small remote launch script first, then start that script inside `tmux` or `screen`. This makes the exact command auditable and avoids silent quoting bugs.

If `tmux` is missing but `screen` is present:

```bash
screen -dmS exp-<short-name> bash -lc 'cd <remote-workdir> && <env-bootstrap> && <run-command> >> logs/<short-name>.log 2>&1'
screen -ls
tail -n 80 logs/<short-name>.log
```

After launching a detached direct SSH or VM run, verify at least two of these before reporting that it is running:

- the `tmux` or `screen` session exists
- the training process appears in `ps -fu $USER` or `pgrep -af <process-pattern>`
- `nvidia-smi` shows a matching process or GPU memory allocation
- the log file is being written and does not show an immediate traceback

Wait 10-30 seconds after launch before the first confirmation unless the command is expected to exit quickly. If the command exits immediately, treat that as a failed launch: capture the last log lines, identify the likely cause, and either fix and relaunch if the fix is clear or report the blocker.

### Interactive Slurm debug

Use this when the user wants to poke at the environment, validate CUDA visibility, or debug a broken job script.

Typical shape:

```bash
ssh <login-alias>
srun --pty -p <partition> --gres=gpu:<n> --cpus-per-task=<n> --mem=<mem> --time=<hh:mm:ss> bash
cd <workdir>
<env-bootstrap>
<run-command>
```

### Batch Slurm run

Use a job script when the work should survive logout or wait in queue cleanly.

Start from [`assets/slurm-job-template.sh`](assets/slurm-job-template.sh), adapt it to the site policy, and save logs to a predictable location such as `logs/%x-%j.out`.

Typical lifecycle:

```bash
ssh <login-alias>
cd <workdir>
mkdir -p logs
sbatch job.sh
squeue -u $USER
sacct -j <jobid> --format=JobID,State,Elapsed,MaxRSS,ExitCode
```

If the cluster needs `--account`, `--qos`, `--constraint`, `--nodes`, `--ntasks-per-node`, `--gpus-per-node`, or site-specific module loads, prefer the values from the machine inventory or site defaults rather than guessing.

After `sbatch`, report the job as submitted only after capturing the job id. Report it as running only if `squeue`, `scontrol`, or `sacct` shows an appropriate state. If it is pending, report the pending reason and log path instead of implying GPUs are already in use.

## Environment bootstrap

Before launching experiments, confirm the remote environment in the lightest way that can still succeed:

- repo path or shared project path
- package manager: conda, mamba, uv, pip, poetry, or modules
- CUDA and driver visibility
- writable output directory

Typical checks:

```bash
pwd
which python
python --version
nvidia-smi
```

For shared HPC systems, account for module systems:

```bash
module avail
module load cuda/<version>
```

## Monitoring and recovery

Always leave the run observable.

For direct SSH hosts and VMs:

- `tmux ls`
- `tmux capture-pane -pt <session> -S -80`
- `screen -ls`
- `tail -f <logfile>`
- `ps -fp <pid>`
- `pgrep -af <process-pattern>`
- `nvidia-smi`

For Slurm:

- `squeue -u $USER`
- `scontrol show job <jobid>`
- `sacct -j <jobid> --format=JobID,JobName,Partition,State,Elapsed,ExitCode`
- `tail -f logs/<job-log>`

If a run fails, collect the smallest set of evidence that explains the failure:

- exact command or job script
- scheduler state and exit code
- stderr or last lines of the log
- environment mismatch such as missing module, wrong Python, missing checkpoint path, or disk quota exhaustion

## Safety rules

Follow these every time:

- Do not reboot, power-cycle, or reimage any machine unless the user explicitly asks.
- Do not kill other users' jobs.
- Do not clear shared scratch, shared logs, or checkpoints without confirmation.
- Do not run heavy training directly on login nodes.
- Do not assume root access on any machine.
- Do not assume VM host-level control just because the guest is reachable.
- Do not print secrets, OTP seeds, SSH private keys, or long tokens back to the chat.
- Do not rewrite `~/.ssh/config` or swap a machine's key mapping unless the user asks.
- Do not use application-gated resources such as A800 nodes unless the inventory or user confirms current approval.
- Do not write Bitwarden passwords, TOTP seeds, current TOTP codes, or private-key contents into inventory files.

## Output format

When you act on a task with this skill, report the result in a compact operational summary:

1. Target machine and why it was selected
2. Access path and auth pattern
3. Commands executed or the exact commands prepared for the user
4. Where logs, checkpoints, and outputs live
5. The next command the user will probably want

## Helpful bundled files

- [`assets/machine-inventory.template.yaml`](assets/machine-inventory.template.yaml): starter inventory for this kind of lab environment
- [`assets/slurm-job-template.sh`](assets/slurm-job-template.sh): generic Slurm batch template
- [`scripts/discover_ssh_hosts.py`](scripts/discover_ssh_hosts.py): summarize likely SSH aliases from local config
- [`scripts/bw_lab_secret.py`](scripts/bw_lab_secret.py): local Bitwarden CLI wrapper for passwords, TOTP, item JSON, and attachment fallback
- [`evals/evals.json`](evals/evals.json): behavior checks covering direct SSH, TOTP, Bitwarden SSH Agent, jump hosts, tmux, and Slurm
