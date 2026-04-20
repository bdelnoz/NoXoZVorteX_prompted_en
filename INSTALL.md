<!--
Document : INSTALL.md
Auteur : Bruno DELNOZ
Email : bruno.delnoz@protonmail.com
Version : v1.0.0
Date : 2026-04-20 11:35
-->
# Installation Guide

## Requirements

- Python 3.8+
- `pip`
- Internet connection for API-based execution
- A valid `MISTRAL_API_KEY` for non-simulated execution

## Installation steps

```bash
# From repository root
./analyse_conversations_merged.py --install
```

Then verify:

```bash
./analyse_conversations_merged.py --prerequis
```

## API key setup

```bash
export MISTRAL_API_KEY='your_api_key'
```

## First verification run (dry-run)

```bash
./analyse_conversations_merged.py --exec \
  --simulate \
  --aiall \
  --fichier ./data_example/*.json \
  --prompt-file example_security_prompt \
  --format markdown
```

## Optional: run project tests

```bash
python3 test_features.py
```
