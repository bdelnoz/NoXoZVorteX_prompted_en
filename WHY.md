<!--
Document : WHY.md
Auteur : Bruno DELNOZ
Email : bruno.delnoz@protonmail.com
Version : v1.0.0
Date : 2026-04-20 11:35
-->
# Why this project exists

## Problem

Exported AI conversations are often large, inconsistent across providers, and difficult to analyze manually at scale.

## Goal

Provide a single CLI workflow that can:

- load ChatGPT, Claude, and LeChat/Mistral exports,
- apply a reusable custom prompt strategy,
- generate structured reports in multiple formats,
- support safe testing through simulation mode.

## Design principles

- Prompt-driven analysis (`prompt_*.txt` files).
- Multi-format source support with auto-detection.
- Traceable results via logs and output files.
- Reproducible CLI execution for operational use.

## Current scope

- Batch processing from JSON exports.
- Prompt file or inline prompt execution.
- CSV/JSON/TXT/Markdown outputs.
- Optional filtering/dedup controls (`--cnbr`, `--only-split`, `--not-split`, `--max-big-conv`, `--no-dedup`).

## Non-goals (current state)

- No web UI in this repository.
- No local offline LLM engine in the current main flow.
