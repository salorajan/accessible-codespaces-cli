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

## 2. Test Execution

### Command: Run Unit Tests
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:26:21`  
**Output:**
```text
test_accessible_summary_output (test_data_analyzer.TestCSVAnalyzer.test_accessible_summary_output) ... ok
test_analysis_stats (test_data_analyzer.TestCSVAnalyzer.test_analysis_stats) ... ok
test_imputation_auto (test_data_analyzer.TestCSVAnalyzer.test_imputation_auto) ... ok
test_missing_token_detection (test_data_analyzer.TestCSVAnalyzer.test_missing_token_detection) ... ok
test_try_parse_float (test_data_analyzer.TestCSVAnalyzer.test_try_parse_float) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.009s

OK
```

---

## 3. Application Execution

### Command: Run CSV Missing Value Analyzer & Imputer CLI
```powershell
python -m src.cli -i data/sample_data.csv -o data/cleaned_data.csv -s auto
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:26:59`  
**Output:**
```text
============================================================
DATASET MISSING VALUE ANALYSIS REPORT
============================================================
Source File: sample_data.csv
Total Rows: 15
Total Columns: 7
------------------------------------------------------------
Total Missing Cells: 13 out of 105 (12.38%)
------------------------------------------------------------
Column Details:
Column 1: id
  Type: numeric
  Missing: 0 of 15 rows (0.0%)
  Mean: 8.0, Median: 8.0, Range: [1.0 to 15.0]

Column 2: name
  Type: text
  Missing: 0 of 15 rows (0.0%)
  Most Frequent (Mode): 'Alice', Unique Values: 15

Column 3: department
  Type: text
  Missing: 3 of 15 rows (20.0%)
  Most Frequent (Mode): 'Engineering', Unique Values: 3

Column 4: age
  Type: numeric
  Missing: 3 of 15 rows (20.0%)
  Mean: 34.5, Median: 32.0, Range: [26.0 to 50.0]

Column 5: salary
  Type: numeric
  Missing: 3 of 15 rows (20.0%)
  Mean: 79833.33, Median: 80000.0, Range: [58000.0 to 105000.0]

Column 6: performance_score
  Type: numeric
  Missing: 3 of 15 rows (20.0%)
  Mean: 4.17, Median: 4.15, Range: [3.5 to 4.9]

Column 7: city
  Type: text
  Missing: 1 of 15 rows (6.67%)
  Most Frequent (Mode): 'New York', Unique Values: 4

============================================================
============================================================
IMPUTATION COMPLETED SUCCESSFULLY
============================================================
Cleaned dataset saved to: C:\salo\acb\code_spaces\space\data\cleaned_data.csv
Imputation Actions Taken:
 - Column 'department': Imputed 3 missing cell(s) using 'mode' strategy (Value: Engineering)
 - Column 'age': Imputed 3 missing cell(s) using 'mean' strategy (Value: 34.5)
 - Column 'salary': Imputed 3 missing cell(s) using 'mean' strategy (Value: 79833.33)
 - Column 'performance_score': Imputed 3 missing cell(s) using 'mean' strategy (Value: 4.17)
 - Column 'city': Imputed 1 missing cell(s) using 'mode' strategy (Value: New York)
============================================================
```

---

## 4. Git Repository Initialization & Commit

### Command: Git Initialization & Status
```powershell
git init; git status
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:39:37`  
**Output:**
```text
Initialized empty Git repository in C:/salo/acb/code_spaces/space/.git/
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.devcontainer/
	.gitignore
	LICENSE
	README.md
	TUTORIAL.md
	data/
	plan.md
	prompt0.txt
	report.md
	src/
	tests/

nothing added to commit but untracked files present (use "git add" to track)
```

---

### Command: Git Add & Initial Commit
```powershell
git add .; git commit -m "feat: accessible codespaces educational tutorial and CSV missing value analyzer"
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:40:14`  
**Output:**
```text
[master (root-commit) fb36b1b] feat: accessible codespaces educational tutorial and CSV missing value analyzer
 15 files changed, 1082 insertions(+)
 create mode 100644 .devcontainer/devcontainer.json
 create mode 100644 .gitignore
 create mode 100644 LICENSE
 create mode 100644 README.md
 create mode 100644 TUTORIAL.md
 create mode 100644 data/cleaned_data.csv
 create mode 100644 data/sample_data.csv
 create mode 100644 plan.md
 create mode 100644 prompt0.txt
 create mode 100644 report.md
 create mode 100644 src/__init__.py
 create mode 100644 src/cli.py
 create mode 100644 src/data_analyzer.py
 create mode 100644 tests/__init__.py
 create mode 100644 tests/test_data_analyzer.py
```

---

### Command: Git Log & Final Status Check
```powershell
git log -n 1 --stat; git status
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 04:40:35`  
**Output:**
```text
commit fb36b1b9abe427d23fdd376604a7ab55d0cf167f
Author: Robert Danaraj <salorajan@gmail.com>
Date:   Mon Sep 28 04:40:14 2026 -0700

    feat: accessible codespaces educational tutorial and CSV missing value analyzer

 .devcontainer/devcontainer.json |  35 +++++++
 .gitignore                      |  40 ++++++++
 LICENSE                         |  21 ++++
 README.md                       |  59 +++++++++++
 TUTORIAL.md                     | 177 ++++++++++++++++++++++++++++++++
 data/cleaned_data.csv           |  16 +++
 data/sample_data.csv            |  16 +++
 plan.md                         |  94 +++++++++++++++++
 prompt0.txt                     | 172 +++++++++++++++++++++++++++++++
 report.md                       |  57 +++++++++++
 src/__init__.py                 |   3 +
 src/cli.py                      |  84 +++++++++++++++
 src/data_analyzer.py            | 220 ++++++++++++++++++++++++++++++++++++++++
 tests/__init__.py               |   1 +
 tests/test_data_analyzer.py     |  87 ++++++++++++++++
 15 files changed, 1082 insertions(+)
On branch master
nothing to commit, working tree clean
```

---

## 5. GitHub Remote Publishing & Cloud Codespace Provisioning

### Command: Create Public GitHub Repository & Push
```powershell
gh repo create accessible-codespaces-cli --public --source=. --remote=origin --push
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 07:42:00`  
**Output:**
```text
✓ Created repository salorajan/accessible-codespaces-cli on github.com
  https://github.com/salorajan/accessible-codespaces-cli
✓ Added remote https://github.com/salorajan/accessible-codespaces-cli.git
Enumerating objects: 30, done.
Counting objects: 100% (30/30), done.
Delta compression using up to 16 threads
Compressing objects: 100% (28/28), done.
Writing objects: 100% (30/30), 25.70 KiB | 4.28 MiB/s, done.
Total 30 (delta 5), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (5/5), done.
To https://github.com/salorajan/accessible-codespaces-cli.git
 * [new branch]      HEAD -> master
branch 'master' set up to track 'origin/master'.
✓ Pushed commits to https://github.com/salorajan/accessible-codespaces-cli.git
```

---

### Command: Verify Remote Configuration
```powershell
git remote -v
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 07:42:30`  
**Output:**
```text
origin  https://github.com/salorajan/accessible-codespaces-cli.git (fetch)
origin  https://github.com/salorajan/accessible-codespaces-cli.git (push)
```

---

### Command: Provision Cloud Codespace VM via CLI
```powershell
gh cs create --repo salorajan/accessible-codespaces-cli --branch master --machine standardLinux32gb --display-name cs-python-dev
```
**Exit Code:** `0`  
**Timestamp:** `2026-09-28 07:43:00`  
**Output:**
```text
  ✓ Codespaces usage for this repository is paid for by salorajan
cs-python-dev-7g9xrq59vjcpjwg
```

