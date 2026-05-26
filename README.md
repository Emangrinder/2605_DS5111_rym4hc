# SoftAutoS26rym4hc

# AWS VM Bootstrap & Development Environment Setup

This repository contains scripts and configurations to automate the provisioning of an Ubuntu Server 26.04 instance on AWS EC2, configure GitHub credentials, and establish a reproducible Python 3.14 development environment using a `makefile`.

By automating this sequence, our development environment becomes completely ephemeral and fault-tolerant. If a cloud instance crashes, it can be cloned or recreated from scratch within minutes.

---

## 🚀 Quick Start / Setup Sequence

### Prerequisites
Before running the setup, ensure you meet the following baseline conditions:
1. You have provisioned a fresh **Ubuntu Server 26.04** VM on AWS EC2.
2. Your VM instance is named strictly following the convention: `<first_name>_<UVAID>` (e.g., `emmett_eh1234`).
3. You have configured an SSH key on this VM that connects successfully to GitHub.

---

### 1. Replicate & Initialize the Machine
Run the base system setup to bring your package snapshots up to date and install critical system-level tools (`make`, `python3.14-venv`, and `tree`).

```bash
# 1. Download or create your initialization script
nano init.sh
