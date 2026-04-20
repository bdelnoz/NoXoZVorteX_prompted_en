<!--
Document : README.md
Auteur : Bruno DELNOZ
Email : bruno.delnoz@protonmail.com
Version : v3.1.0
Date : 2026-04-20 11:35
-->
# NoXoZVorteX_prompted

AI Conversation Prompt Executor for exported conversations from ChatGPT, Claude, and LeChat/Mistral, with customizable prompts and multi-format reports.

## Project status

- Main executable: `analyse_conversations_merged.py` (version reported by script/help: `v3.0.2`).
- Supported sources: ChatGPT, Claude, LeChat/Mistral JSON exports.
- Output formats: `csv`, `json`, `txt`, `markdown`.
- Prompt modes: prompt file (`prompts/prompt_<name>.txt`) or inline prompt (`--prompt-text`).

## Repository layout

- `analyse_conversations_merged.py`: main CLI and orchestration.
- `config.py`: defaults and API key lookup.
- `extractors.py`: source format detection and message extraction.
- `prompt_executor.py`: prompt execution logic.
- `result_formatter.py`: result export formatting.
- `utils.py`: utilities (token counting and helpers).
- `install.py`: dependency and prerequisite helpers.
- `help.py` + `help_advanced.txt`: CLI help content.
- `test_features.py`: functional test runner.
- `prompts/`: reusable prompt templates.
- `data_example/`: example exported conversation files.

## CLI reference (synchronized with current script)

### Core actions

- `--help`
- `--help-adv`
- `--exec`
- `--install`
- `--prerequis`
- `--changelog`

### Source selection

- `--chatgpt`
- `--lechat`
- `--claude`
- `--aiall` / `--auto`
- `--fichier`, `-F <files...>`
- `--recursive`

### Prompt options

- `--prompt-file`, `-p <name>`
- `--prompt-list`
- `--prompt-text`, `-pt <text>`

### Processing controls

- `--simulate`
- `--workers`, `-w <N>`
- `--delay`, `-d <seconds>`
- `--cnbr <N>`
- `--only-split`
- `--not-split`
- `--max-big-conv <N>`
- `--no-dedup`

### Output and model

- `--model`, `-m <model>`
- `--format <csv|json|txt|markdown>`
- `--output`, `-o <file>`
- `--target-logs <dir>`
- `--target-results <dir>`

## Quick start

```bash
# 1) Install dependencies and local environment helpers
./analyse_conversations_merged.py --install

# 2) Verify prerequisites
./analyse_conversations_merged.py --prerequis

# 3) Set API key
export MISTRAL_API_KEY='your_api_key'

# 4) List prompts
./analyse_conversations_merged.py --prompt-list

# 5) Run a simulation first
./analyse_conversations_merged.py --exec \
  --simulate \
  --aiall \
  --fichier ./data_example/*.json \
  --prompt-file example_security_prompt \
  --target-logs ./logs_example \
  --target-results ./results_example \
  --format markdown
```

## Prompt template reminder

Prompt files live in `prompts/` and follow `prompt_<name>.txt` naming.

Minimal structure:

```text
---SYSTEM---
You are an expert analyst.

---USER---
Analyze: {TITLE}
Messages: {MESSAGE_COUNT}
Tokens: {TOKEN_COUNT}

{CONVERSATION_TEXT}
```

Variables supported by the current implementation:

- `{CONVERSATION_TEXT}`
- `{TITLE}`
- `{MESSAGE_COUNT}`
- `{TOKEN_COUNT}`
- `{FORMAT}`
- `{FILE}`

## Documentation index

- `EXECUTABLE_FILES_GUIDE.md`: runnable files and practical command map.
- `INSTALL.md`: installation and dependency guidance.
- `WHY.md`: project purpose and design rationale.
- `CHANGELOG.md`: version and change history.

## License

MIT license (`LICENSE`).
