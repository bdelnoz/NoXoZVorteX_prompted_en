<!--
Document : EXECUTABLE_FILES_GUIDE.md
Auteur : Bruno DELNOZ
Email : bruno.delnoz@protonmail.com
Version : v3.1.0
Date : 2026-04-20 11:35
-->
# NoXoZVorteX_prompted - Executable Files Guide

## Executable files

### 1) `analyse_conversations_merged.py` (main entrypoint)

This is the primary executable for normal project usage.

Run:

```bash
./analyse_conversations_merged.py [OPTIONS]
# or
python3 analyse_conversations_merged.py [OPTIONS]
```

Main commands:

- `--install`: install dependencies / environment support.
- `--prerequis`: verify prerequisites.
- `--help` / `--help-adv`: display help.
- `--prompt-list`: list prompts from `prompts/`.
- `--exec`: execute analysis.
- `--changelog`: show changelog information.

Additional execution options currently available in the script:

- Source/format: `--chatgpt`, `--claude`, `--lechat`, `--aiall`, `--recursive`, `--fichier`.
- Prompting: `--prompt-file`, `--prompt-text`, `--prompt-list`.
- Filtering: `--cnbr`, `--only-split`, `--not-split`, `--max-big-conv`, `--no-dedup`.
- Runtime: `--simulate`, `--workers`, `--delay`, `--model`.
- Output: `--format`, `--output`, `--target-logs`, `--target-results`.

### 2) `test_features.py` (test runner)

Use this file to run the project feature tests.

Run:

```bash
python3 test_features.py
```

What it validates:

- Main CLI availability and help commands.
- Prompt and changelog command behavior.
- End-to-end test setup for repository features.

Recommended moments to run tests:

- after installation,
- after any functional change,
- before preparing a release.

## Non-executable support modules

These files are imported by the main script and are not intended to be run directly:

- `config.py`
- `extractors.py`
- `prompt_executor.py`
- `result_formatter.py`
- `utils.py`
- `install.py`
- `help.py`

## Typical workflow

```bash
# 1) Install and check prerequisites
./analyse_conversations_merged.py --install
./analyse_conversations_merged.py --prerequis

# 2) Configure API key
export MISTRAL_API_KEY='your_api_key'

# 3) Dry-run first (recommended)
./analyse_conversations_merged.py --exec \
  --simulate \
  --aiall \
  --fichier ./data_example/*.json \
  --prompt-file example_security_prompt \
  --target-logs ./logs_example \
  --target-results ./results_example \
  --format markdown
```

## Frequent errors and fixes

### Permission denied

```bash
chmod +x analyse_conversations_merged.py
```

### Missing Python package

```bash
./analyse_conversations_merged.py --install
```

### Missing API key

```bash
export MISTRAL_API_KEY='your_api_key'
```
