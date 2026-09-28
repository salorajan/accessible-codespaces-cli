# Terminal Command & Execution Audit Report

This report records all terminal commands executed during the setup, testing, and deployment of the Accessible GitHub Codespaces educational project on Windows.

---

## 1. System & Environment Audit

### Command: Tool Versions Check
```powershell
gh --version; git --version; ssh -V; python --version
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:03:19`  
**Output:**
```text
gh version 2.87.3 (2026-02-23)
https://github.com/cli/cli/releases/tag/v2.87.3
git version 2.55.0.windows.1
OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2
Python 3.14.7
```

---

### Command: GitHub CLI Authentication Check
```powershell
gh auth status
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:05:24`  
**Output:**
```text
github.com
  ✓ Logged in to github.com account salorajan (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'delete_repo', 'gist', 'read:org', 'repo', 'workflow'
```

---

### Command: Codespace Scope Verification Check
```powershell
gh cs list
```
**Exit Code:** `1`  
**Timestamp:** `2026-09-28 04:06:24`  
**Output:**
```text
error getting codespaces: HTTP 403: Must have admin rights to Repository. (https://api.github.com/user/codespaces?per_page=30)
This API operation needs the "codespace" scope. To request it, run:  gh auth refresh -h github.com -s codespace
```
**Audit Note:** To manage Codespaces via GitHub CLI, the active token requires the `codespace` scope. In user sessions, run `gh auth refresh -h github.com -s codespace` to grant this scope.

---
