(2508_DS5111) SoftAutoS26rym4hc — VM Setup

This README walks a new user through getting a fresh VM ready to work on this project.

## Prerequisites / Starting point

Before following these steps you should have:
- A fresh Ubuntu Server 26.04 VM that you can SSH into
- A GitHub SSH key already set up on the VM (so `git clone` over SSH works)

## Setup steps

### 1. Clone the repository
From your home directory on the VM:
```bash
git clone git@github.com:emangrinder/2508_DS5111_.git
cd 2508_DS5111_
```

### 2. Run the bootstrap script
This updates apt and installs `make`, `python3.14-venv`, and `tree`:
```bash
cd scripts
bash init.sh
cd ..
```
**Quick test:** run `tree` from anywhere — if it lists files instead of throwing "command not found," it worked.

### 3. Configure git credentials
This tags your commits with the right email and username:
```bash
cd scripts
bash init_git_creds.sh
cd ..
```
**Quick test:** the script echoes the global git config before and after. You should see:
- `user.email=emmett.hannam@gmail.com`
- `user.name=emangrinder`

### 4. Build the Python virtual environment
From the repo root:
```bash
make update
```
This creates `env/`, upgrades pip, and installs everything in `requirements.txt`.

**Quick test:**
```bash
. env/bin/activate
pip list
```
You should see `(env)` in your prompt and `pandas` and `numpy` listed.

## Summary
After running the three commands above (`bash init.sh`, `bash init_git_creds.sh`, `make update`), the VM is ready for development.
