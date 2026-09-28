# Accessible GitHub Codespaces via CLI: Complete Screen Reader Guide

This educational guide demonstrates how to provision, configure, develop inside, and tear down GitHub Codespaces exclusively from the Windows Terminal using the GitHub CLI (`gh`), Git, and OpenSSH.

This tutorial is optimized for developers using screen readers (NVDA, JAWS, or Windows Narrator). All procedures use non-interactive command-line arguments to eliminate interactive arrow-key selection traps.

---

## 1. Prerequisites and Initial Verification

Before creating cloud containers, verify that your local Windows host has the required command-line tools installed.

### 1.1 Local Tools Verification
Open PowerShell in Windows Terminal and execute:

```powershell
gh --version
git --version
ssh -V
python --version
```

- **GitHub CLI (`gh`)**: Version 2.45.0 or higher is recommended.
- **Git**: Version 2.40.0 or higher.
- **OpenSSH**: OpenSSH for Windows (`ssh -V`) is required to open secure shell sessions into your Codespace.
- **Python**: Python 3.10+ for local script execution and test runs.

### 1.2 GitHub Authentication and Scope Verification
Verify that your local `gh` CLI session has permission to manage Codespaces:

```powershell
gh auth status
```

If the `Token scopes` list does not include `'codespace'`, refresh your authentication with:

```powershell
gh auth refresh -h github.com -s codespace
```

---

## 2. Codespace Creation via Non-Interactive CLI

When using a screen reader, avoid interactive prompts that require visual arrow navigation. Always supply explicit flags.

### 2.1 Provisioning a New Codespace
Use the following command format:

```powershell
gh cs create --repo <username>/<repository-name> --branch main --machine standardLinux32gb --display-name cs-python-dev
```

- `--repo`: Target GitHub repository (e.g., `salorajan/accessible-codespaces-cli`).
- `--branch`: Target branch (default `main`).
- `--machine`: Compute tier (e.g., `standardLinux32gb` for 2 cores / 8GB RAM / 32GB disk).
- `--display-name`: A custom readable name instead of GitHub's random auto-generated words (e.g., `cs-python-dev`).

---

## 3. Querying and Inspecting Cloud Workspaces

### 3.1 Listing Active Codespaces
To list all codespaces associated with your account:

```powershell
gh cs list
```

### 3.2 Reading Structured JSON Data
For predictable reading with screen readers or programmatic scripts:

```powershell
gh cs view -c <codespace-name> --json name,state,machineDisplayName,createdAt
```

---

## 4. Connecting to the Codespace via OpenSSH

The core remote development workflow takes place directly over an encrypted SSH connection.

### 4.1 Initiating the SSH Connection
Run:

```powershell
gh cs ssh -c <codespace-name>
```

### 4.2 Screen Reader Review Navigation Inside SSH
Once connected, your terminal prompt changes to the Linux environment (e.g., `vscode@codespace:/workspaces/accessible-codespaces-cli$ `).

- **NVDA Users**:
  - Switch between **Focus Mode** (typing directly into the bash shell) and **Browse Mode** using `NVDA + Space`.
  - Use **Review Mode** (`Numpad 7`, `Numpad 8`, `Numpad 9` for Desktop layout, or `NVDA + Up/Down/Left/Right`) to read previous terminal output line-by-line without re-executing commands.
- **JAWS Users**:
  - Use `Insert + Z` or `NumPad Plus` to toggle the Virtual PC Cursor on/off for terminal buffer review.

### 4.3 Executing Python Commands Inside the Cloud Container
Run the CSV data analysis script directly on the cloud VM:

```bash
python3 -m src.cli -i data/sample_data.csv -o data/cleaned_data.csv -s auto
```

Run test suite:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Exit the SSH session back to Windows:

```bash
exit
```

---

## 5. File Synchronization Between Local Host and Cloud

You can push or pull files without graphical file explorers.

### 5.1 Copying a Local File to the Remote Codespace
```powershell
gh cs cp ./data/sample_data.csv remote:/workspaces/accessible-codespaces-cli/data/sample_data.csv -c <codespace-name>
```

### 5.2 Downloading Remote Artifacts to Local Disk
```powershell
gh cs cp remote:/workspaces/accessible-codespaces-cli/data/cleaned_data.csv ./data/remote_cleaned_data.csv -c <codespace-name>
```

---

## 6. Port Forwarding for Web & API Testing

If you run a local web server (such as Flask, FastAPI, or a documentation previewer) inside the Codespace on port 8000:

```powershell
gh cs ports forward 8000:8000 -c <codespace-name>
```

Your Windows browser or curl client can now reach the cloud application at `http://localhost:8000`.

---

## 7. Lifecycle Management and Quota Hygiene

GitHub Free accounts receive a monthly allotment of core-hours (typically 120 core-hours) and storage (15 GB-month). Stopping and deleting unused containers prevents quota exhaustion.

### 7.1 Stopping a Running Codespace
To pause compute consumption while preserving disk contents:

```powershell
gh cs stop -c <codespace-name>
```

### 7.2 Deleting a Codespace (Releasing Disk Storage)
To completely delete the instance and prevent storage billing:

```powershell
gh cs delete -c <codespace-name> --confirm
```

The `--confirm` flag bypasses the interactive confirmation prompt.

---

## 8. Screen Reader Tips & Edge-Case Troubleshooting

1. **Dealing with ANSI Escape Sequences**:
   - The `.devcontainer/devcontainer.json` configuration in this repo sets `NO_COLOR=1` and `PAGER=cat` to prevent ANSI colors and interactive pagers from confusing screen readers.
2. **First-time SSH Key Generation**:
   - The first time `gh cs ssh` runs, it creates an OpenSSH key in `~/.ssh/`. If a permission error occurs on Windows, verify that `C:\Users\<Username>\.ssh` exists and has standard user read/write access.
3. **Deterministic Display Names**:
   - Always assign a meaningful name via `--display-name` during creation to make screen-reader speech announcements clear and easily distinguishable.
