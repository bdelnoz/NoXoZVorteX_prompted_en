#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Help Module
Displays standard help, advanced help and changelog
"""

import os
from pathlib import Path
from config import VERSION, MAX_TOKENS, MAX_WORKERS, MODEL


def afficher_aide() -> None:
    """Displays standard script help."""
    aide = f"""
╔═══════════════════════════════════════════════════════════════╗
║  AI Conversation Prompt Executor {VERSION}                     ║
╚═══════════════════════════════════════════════════════════════╝

Version: {VERSION}
Author: Bruno DELNOZ

## DESCRIPTION
Custom prompt execution engine for AI conversations.
Supports ChatGPT, Claude and LeChat/Mistral.

## API CONFIGURATION
export MISTRAL_API_KEY='your_api_key'

## MAIN OPTIONS
  --help              Display this help
  --help-adv          Display complete advanced help ⭐
  --exec              Start analysis
  --install           Install dependencies
  --prerequis         Check prerequisites
  --changelog         Display changelog

## SUPPORTED FORMATS
  --chatgpt           ChatGPT export format
  --lechat            LeChat export format (Mistral)
  --claude            Claude export format
  --aiall, --auto     Auto-detection of ALL formats

## PROMPTS ⭐ NEW
  --prompt-file FILE  Prompt file to use (in prompts/)
  --prompt-list       List all available prompts
  --prompt-text TEXT  Direct command line prompt

## DATA SOURCES
  --fichier, -F FILE  JSON file(s) (supports *.json)
  --recursive         Recursive search in subfolders

## EXECUTION OPTIONS
  --model, -m MODEL   Mistral model (default: {MODEL})
  --workers, -w N     Parallel workers (default: {MAX_WORKERS})
  --simulate          Simulation mode (no API call)

## FILE ORGANIZATION ⭐ NEW
  --target-logs DIR   Logs folder (default: ./)
  --target-results    Results folder (default: ./)
  --format FORMAT     csv, json, txt, markdown (default: csv)
  --output, -o FILE   Custom output filename

## QUICK EXAMPLES

1. List available prompts:
   python analyse_conversations_merged.py --prompt-list

2. Simple analysis with prompt:
   python analyse_conversations_merged.py --exec \\
     --aiall --fichier *.json \\
     --prompt-file resume

3. Complete organization:
   python analyse_conversations_merged.py --exec \\
     --prompt-file security_analysis \\
     --fichier data/*.json \\
     --target-logs ./logs \\
     --target-results ./results \\
     --format markdown

4. Simulation mode (test without API):
   python analyse_conversations_merged.py --exec \\
     --simulate --prompt-file test \\
     --fichier export.json

💡 For more details and examples: --help-adv
📚 Complete documentation: see STRUCTURE.md
"""
    print(aide)


def afficher_aide_avancee() -> None:
    """Displays complete advanced help from help_advanced.txt."""
    help_file = Path("help_advanced.txt")

    if help_file.exists():
        try:
            with open(help_file, 'r', encoding='utf-8') as f:
                contenu = f.read()
            print(contenu)
        except Exception as e:
            print(f"❌ Error reading help_advanced.txt: {e}")
            afficher_aide_avancee_integree()
    else:
        print(f"⚠️  File help_advanced.txt not found")
        print(f"💡 Creating file with default content...\n")
        creer_help_advanced_defaut()
        afficher_aide_avancee_integree()


def afficher_aide_avancee_integree() -> None:
    """Displays integrated advanced help if file doesn't exist."""
    aide_avancee = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║             AI CONVERSATION PROMPT EXECUTOR - ADVANCED HELP                   ║
║                           Version {VERSION}                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
📋 TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════════════════════

1. Detailed arguments
2. Prompt management
3. Available variables
4. Output formats
5. Advanced examples
6. Troubleshooting

═══════════════════════════════════════════════════════════════════════════════
1. DETAILED ARGUMENTS
═══════════════════════════════════════════════════════════════════════════════

## Main arguments
  --help              Standard help (quick)
  --help-adv          This help (complete)
  --exec              Execute processing
  --install           Install dependencies in .venv_analyse
  --prerequis         Check Python >= 3.8, permissions, modules
  --changelog         Version history

## Source formats
  --chatgpt           Force ChatGPT format
  --lechat            Force LeChat/Mistral format
  --claude            Force Claude format
  --aiall / --auto    Auto-detection (recommended)

## Prompts (REQUIRED with --exec)
  --prompt-file FILE  Load prompts/prompt_FILE.txt
                      Examples: resume, security_analysis, child_safety_analysis
  --prompt-list       List all available prompts/
  --prompt-text TEXT  Direct prompt without file

## Data sources
  --fichier, -F       One or more JSON files
                      Supports wildcards: *.json, data/*.json
  --recursive         Recursive search in subfolders
                      Combined with --fichier to search everywhere

## Filters
  --cnbr N            Analyze only conversation N
  --only-split        Only conversations > {MAX_TOKENS} tokens
  --not-split         Only conversations ≤ {MAX_TOKENS} tokens

## Execution
  --model, -m MODEL   Mistral model (default: {MODEL})
  --workers, -w N     Parallel workers (default: {MAX_WORKERS})
  --delay, -d SEC     Delay between requests (default: 0.5s)
  --simulate          Dry-run mode (no API call)

## File organization
  --target-logs DIR   Logs folder (auto-created if missing)
  --target-results    Results folder (auto-created if missing)
  --format FORMAT     csv | json | txt | markdown
  --output, -o FILE   Custom output filename

═══════════════════════════════════════════════════════════════════════════════
2. PROMPT MANAGEMENT
═══════════════════════════════════════════════════════════════════════════════

## Prompt structure

Prompts are text files in prompts/ with the prompt_ prefix

Example: prompts/prompt_resume.txt

### Simple format:
```
You are an expert in [DOMAIN].

Analyze this conversation and [OBJECTIVE].

Conversation:
{{{{CONVERSATION_TEXT}}}}

Output format:
[Instructions]
```

### Advanced format (SYSTEM/USER):
```
---SYSTEM---
You are an expert in [DOMAIN] with [EXPERIENCE].
Your skills: [LIST]

---USER---
# [TYPE] ANALYSIS

## CONTEXT
- Title: {{TITLE}}
- Messages: {{MESSAGE_COUNT}}
- Tokens: {{TOKEN_COUNT}}
- Format: {{FORMAT}}
- File: {{FILE}}

## MISSION
[Detailed instructions]

Conversation:
{{CONVERSATION_TEXT}}
```

## Available variables

In your prompts, use these variables in curly braces:

- {{CONVERSATION_TEXT}}  - Complete conversation text
- {{TITLE}}              - Conversation title
- {{MESSAGE_COUNT}}      - Number of messages
- {{TOKEN_COUNT}}        - Number of tokens
- {{FORMAT}}             - Source format (CHATGPT/LECHAT/CLAUDE)
- {{FILE}}               - Source filename

## Default provided prompts

- prompt_resume.txt              - 3-point summary
- prompt_extract_topics.txt      - List of topics
- prompt_questions.txt           - Questions asked
- prompt_security_analysis.txt   - Complete security analysis
- prompt_child_safety_analysis.txt - Children's content safety

═══════════════════════════════════════════════════════════════════════════════
3. OUTPUT FORMATS
═══════════════════════════════════════════════════════════════════════════════

## CSV (default)
Columns: conversation_id, titre, partie, response, success, error,
          token_count, fichier_source, format, model_used

Advantages: Excel/LibreOffice compatible, easy to filter

## JSON
Hierarchical structure with all fields
Advantages: Easy to parse, type preserved

## TXT
Readable format with visual separators
Advantages: Direct reading, no tool needed

## Markdown
Format with table of contents, metadata, statistics
Advantages: GitHub preview, PDF/HTML export

═══════════════════════════════════════════════════════════════════════════════
4. ADVANCED EXAMPLES
═══════════════════════════════════════════════════════════════════════════════

## Example 1: Complete security workflow
```bash
# 1. Installation
python analyse_conversations_merged.py --install

# 2. Check
python analyse_conversations_merged.py --prerequis

# 3. List prompts
python analyse_conversations_merged.py --prompt-list

# 4. Security analysis on all JSON
export MISTRAL_API_KEY='your_key'
python analyse_conversations_merged.py --exec \\
  --aiall --recursive \\
  --fichier ./data/ \\
  --prompt-file security_analysis \\
  --target-logs ./logs/security \\
  --target-results ./reports/security \\
  --format markdown \\
  --workers 10
```

## Example 2: Quick test with simulation
```bash
python analyse_conversations_merged.py --exec \\
  --simulate \\
  --prompt-file resume \\
  --fichier test.json \\
  --format json
```

## Example 3: Specific file analysis
```bash
python analyse_conversations_merged.py --exec \\
  --chatgpt \\
  --fichier export_20251026.json \\
  --prompt-file extract_topics \\
  --output topics_report.txt \\
  --format txt
```

## Example 4: Multi-file with filtering
```bash
# Only long conversations
python analyse_conversations_merged.py --exec \\
  --aiall \\
  --fichier data/*.json \\
  --only-split \\
  --prompt-file security_analysis \\
  --target-results ./results/long_conversations
```

## Example 5: Direct prompt without file
```bash
python analyse_conversations_merged.py --exec \\
  --aiall --fichier *.json \\
  --prompt-text "List the 5 main topics of this conversation"
```

## Example 6: Professional organization
```bash
# Recommended structure:
# project/
# ├── data/           (your exports)
# ├── logs/           (generated logs)
# ├── results/        (results)
# └── prompts/        (your prompts)

python analyse_conversations_merged.py --exec \\
  --recursive --aiall \\
  --fichier ./data/ \\
  --prompt-file custom_analysis \\
  --target-logs ./logs/$(date +%Y%m%d) \\
  --target-results ./results/$(date +%Y%m%d) \\
  --format markdown \\
  --workers 15
```

═══════════════════════════════════════════════════════════════════════════════
5. TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

## Problem: "No prompt specified"
Solution: Use --prompt-file <name> or --prompt-text "..."

## Problem: "Prompt not found"
Solutions:
- Check that file exists: prompts/prompt_<name>.txt
- Use --prompt-list to see available prompts
- The prompt_ prefix is automatic: --prompt-file resume is enough

## Problem: "Missing dependencies"
Solutions:
1. Run: python analyse_conversations_merged.py --install
2. Activate venv: source .venv_analyse/bin/activate
3. Rerun your command

## Problem: "API key not defined"
Solution: export MISTRAL_API_KEY='your_key'

## Problem: "Unknown format"
Solutions:
- Use --aiall for auto-detection
- Check your JSON structure
- Consult logs in --target-logs

## Problem: "HTTP 429 error (rate limit)"
Solutions:
- Increase --delay: --delay 1.0
- Reduce --workers: --workers 3
- Wait a few minutes

## Problem: Conversations too long
The script automatically splits conversations > {MAX_TOKENS} tokens
into 2 parts. You can:
- Filter with --only-split or --not-split
- See split conversations in final report

═══════════════════════════════════════════════════════════════════════════════
6. BEST PRACTICES
═══════════════════════════════════════════════════════════════════════════════

## File organization
```
my_project/
├── data/                      # Your JSON exports
│   ├── chatgpt/
│   ├── claude/
│   └── lechat/
├── prompts/                   # Your custom prompts
│   ├── prompt_resume.txt
│   └── prompt_custom.txt
├── logs/                      # Logs (auto-created)
│   └── 2025-10-26/
└── results/                   # Results (auto-created)
    └── 2025-10-26/
```

## Prompt naming
- Always prefix: prompt_<name>.txt
- Use snake_case: prompt_security_analysis.txt
- Be descriptive: prompt_extract_technical_skills.txt

## API security
- Never commit MISTRAL_API_KEY
- Use environment variables
- Test with --simulate first

## Performance
- Start with --workers 5
- Increase gradually according to your machine
- Use --only-split to process long conversations separately

## Recommended workflow
1. --install (once only)
2. --prerequis (check)
3. --prompt-list (see prompts)
4. --simulate (test without API)
5. --exec (real execution)

═══════════════════════════════════════════════════════════════════════════════
📞 SUPPORT
═══════════════════════════════════════════════════════════════════════════════

Author: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: {VERSION}

Complete documentation: see STRUCTURE.md
Changelog: --changelog

═══════════════════════════════════════════════════════════════════════════════
"""
    print(aide_avancee)


def creer_help_advanced_defaut() -> None:
    """Creates help_advanced.txt file with default content."""
    help_file = Path("help_advanced.txt")

    contenu = """╔═══════════════════════════════════════════════════════════════════════════════╗
║             AI CONVERSATION PROMPT EXECUTOR - ADVANCED HELP                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This file can be edited to customize advanced help.
See help.py for complete default content.

To regenerate this file: delete it and run --help-adv again
"""

    try:
        with open(help_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print(f"✅ File {help_file} created successfully\n")
    except Exception as e:
        print(f"❌ Error creating {help_file}: {e}\n")


def afficher_changelog() -> None:
    """Displays complete changelog."""
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           COMPLETE CHANGELOG                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

v3.0.0 (2025-10-26) - MAJOR REFACTORING
  ★ Customizable prompts system (prompt_*.txt)
  ★ Removal of --local mode (API only now)
  ★ --prompt-file: prompt files in prompts/
  ★ --prompt-list: lists all available prompts
  ★ --prompt-text: direct command line prompt
  ★ --help-adv: complete advanced help from help_advanced.txt
  ★ --target-logs: custom folder for logs
  ★ --target-results: custom folder for results
  ★ --format: csv, json, txt, markdown
  ★ Automatic duplicate detection and elimination
  ★ Variables in prompts: {{{{CONVERSATION_TEXT}}}}, {{{{TITLE}}}}, etc.
  ★ SYSTEM/USER prompt support with ---SYSTEM--- / ---USER---
  ★ Automatic folder creation (mkdir -p equivalent)
  ★ prompt_executor.py module: complete prompt management
  ★ result_formatter.py module: multiple output formats
  ★ Simplified architecture: 8 files instead of 12
  ★ Complete STRUCTURE.md documentation

v2.7.5 (2025-10-22):
  - Fix verifier_prerequis import error
  - Final logic correction

v2.7.0 (2025-10-19):
  - Automatic TXT file generation with all topics
  - Ultra-complete operations report
  - Visual split indicator (✂️/✅)
  - Execution time + performance
  - Total disk space used

v2.6.0 (2025-10-19):
  - Complete operations report
  - Detailed split vs non-split statistics
  - File summary table

v2.5.0 (2025-10-19):
  - Multi-format auto-detection
  - Simultaneous ChatGPT/LeChat/Claude support
  - Reinforced AI focus (x3 score)
  - 35+ skill domains
  - Complete logging with rotation

v2.4.0 (2025-10-19):
  - MULTI-FORMAT AUTO-DETECTION
  - --aiall: processes all formats

v2.3.0 (2025-10-18):
  - Maximum priority on AI/ML skills
  - Exhaustive AI detection
  - Automatic categorization

═══════════════════════════════════════════════════════════════════════════════
""")
