# NoXoZVorteX_prompted

**AI Conversation Prompt Executor** - A powerful Python tool for analyzing exported AI conversations (ChatGPT, Claude, LeChat/Mistral) using custom prompts.

[![Version](https://img.shields.io/badge/version-3.0.2-blue.svg)](https://github.com/yourusername/NoXoZVorteX_prompted)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Custom Prompts](#custom-prompts)
- [Output Formats](#output-formats)
- [Project Structure](#project-structure)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This tool allows you to **apply custom analysis prompts** to your exported AI conversations. Instead of manual review, automate the extraction of insights, security analysis, content moderation, or any custom analysis you define.

### Why Use This Tool?

- 🔍 **Analyze** thousands of conversations automatically
- 🛡️ **Security audits** of technical discussions
- 👨‍👩‍👧 **Content safety** assessment for child-related content
- 📊 **Extract insights** like topics, skills, or decisions
- 🤖 **Multi-AI support** - Works with ChatGPT, Claude, and LeChat exports
- 📝 **Custom prompts** - Define your own analysis criteria

---

## ✨ Key Features

### Multi-Format Support
- ✅ **ChatGPT** conversations (JSON export)
- ✅ **Claude** conversations (JSON export)
- ✅ **LeChat/Mistral** conversations (JSON export)
- 🔄 **Auto-detection** of formats

### Powerful Analysis
- 📝 **Custom prompts** via simple text files
- 🎯 **SYSTEM/USER** prompt separation
- 🔄 **Variable substitution** in prompts
- 🧵 **Parallel processing** for speed
- ✂️ **Auto-splitting** of long conversations

### Flexible Output
- 📊 **CSV** - Excel/LibreOffice compatible
- 🗂️ **JSON** - For programmatic processing
- 📄 **TXT** - Simple readable format
- 📑 **Markdown** - With TOC and navigation

### Built-in Safety
- 🔍 **Duplicate detection** and elimination
- 🧪 **Simulation mode** (test without API calls)
- 📋 **Detailed logging** and reports
- ⚡ **Rate limiting** protection

---

## 🚀 Quick Start

### Try the Example Analysis

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/NoXoZVorteX_prompted.git
cd NoXoZVorteX_prompted

# 2. Install dependencies
./analyse_conversations_merged.py --install

# 3. Set your API key
export MISTRAL_API_KEY='your_api_key_here'

# 4. Run example analysis
./analyse_conversations_merged.py --exec \
  --recursive --aiall \
  --fichier ./data_example/ \
  --prompt-file example_security_prompt \
  --target-logs ./logs_example/ \
  --target-results ./results_example/ \
  --format markdown
```

The example will analyze security aspects of sample conversations and generate a detailed Markdown report.

---

## 💾 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls)

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/NoXoZVorteX_prompted.git
cd NoXoZVorteX_prompted

# 2. Run installation (creates virtual environment)
./analyse_conversations_merged.py --install

# 3. Verify installation
./analyse_conversations_merged.py --prerequis

# 4. Configure API key
export MISTRAL_API_KEY='your_mistral_api_key'
```

### Manual Installation (Alternative)

```bash
python3 -m venv .venv_analyse
source .venv_analyse/bin/activate
pip install requests tqdm tiktoken mistletoe anthropic python-dotenv
```

---

## 📚 Usage Examples

### Example 1: Security Analysis

Analyze conversations for security vulnerabilities:

```bash
./analyse_conversations_merged.py --exec \
  --aiall --fichier data/*.json \
  --prompt-file security_analysis \
  --format markdown \
  --target-results ./reports/security
```

### Example 2: Content Moderation

Check conversations for child safety:

```bash
./analyse_conversations_merged.py --exec \
  --recursive --aiall \
  --fichier ./conversations/ \
  --prompt-file child_safety_analysis \
  --format json \
  --workers 10
```

### Example 3: Quick Summary

Get a quick summary of conversations:

```bash
./analyse_conversations_merged.py --exec \
  --aiall --fichier export.json \
  --prompt-file resume \
  --format txt \
  --output summary.txt
```

### Example 4: Test Without API Calls

Test your setup in simulation mode:

```bash
./analyse_conversations_merged.py --exec \
  --simulate \
  --prompt-file test \
  --fichier sample.json
```

---

## 🎨 Custom Prompts

### Creating Your Own Prompt

1. **Create a file** in the `prompts/` directory:
   ```bash
   nano prompts/prompt_my_analysis.txt
   ```

2. **Write your prompt** using available variables:
   ```
   ---SYSTEM---
   You are an expert in [YOUR DOMAIN].
   
   ---USER---
   Analyze this conversation about {TITLE}.
   
   Context:
   - Messages: {MESSAGE_COUNT}
   - Tokens: {TOKEN_COUNT}
   - Format: {FORMAT}
   
   Conversation:
   {CONVERSATION_TEXT}
   
   Provide: [YOUR INSTRUCTIONS]
   ```

3. **Use your prompt**:
   ```bash
   ./analyse_conversations_merged.py --exec \
     --prompt-file my_analysis \
     --fichier data.json
   ```

### Available Variables

| Variable | Description |
|----------|-------------|
| `{CONVERSATION_TEXT}` | Full conversation content |
| `{TITLE}` | Conversation title |
| `{MESSAGE_COUNT}` | Number of messages |
| `{TOKEN_COUNT}` | Token count |
| `{FORMAT}` | Source format (CHATGPT/CLAUDE/LECHAT) |
| `{FILE}` | Source filename |

### List Available Prompts

```bash
./analyse_conversations_merged.py --prompt-list
```

---

## 📊 Output Formats

### CSV Format
```bash
--format csv
```
- Excel/LibreOffice compatible
- Easy filtering and sorting
- Best for: Data analysis, database import

### JSON Format
```bash
--format json
```
- Hierarchical structure
- Preserves all data types
- Best for: Programmatic processing, API integration

### TXT Format
```bash
--format txt
```
- Simple readable text
- Visual separators
- Best for: Quick reading, simple archiving

### Markdown Format
```bash
--format markdown
```
- Clickable table of contents
- Statistics and metadata
- Best for: GitHub, documentation, professional reports

---

## 📁 Project Structure

```
NoXoZVorteX_prompted/
├── analyse_conversations_merged.py    # Main script
├── config.py                          # Configuration
├── extractors.py                      # Message extraction
├── prompt_executor.py                 # Prompt execution
├── result_formatter.py                # Output formatting
├── utils.py                           # Utilities
├── install.py                         # Installation
├── help.py                            # Help system
├── prompts/                           # Custom prompts
│   ├── prompt_example_security_prompt.txt
│   ├── prompt_example_child_safety_prompt.txt
│   └── prompt_example_full_security_analysis_prompt.txt
├── data_example/                      # Example data
│   ├── example_chatgpt_json.json
│   ├── example_claude_json.json
│   └── example_lechat_json.json
├── logs_example/                      # Example logs
├── results_example/                   # Example results
├── README.md                          # This file
├── LICENSE                            # MIT License
└── TRY_THIS_FIRST.txt                # Quick start guide
```

---

## 🔧 Advanced Usage

### Command-Line Options

```bash
# Core Commands
--help              # Basic help
--help-adv          # Advanced help
--exec              # Execute analysis
--install           # Install dependencies
--prerequis         # Check prerequisites

# Prompt Management
--prompt-file NAME  # Use prompt from prompts/
--prompt-text TEXT  # Direct inline prompt
--prompt-list       # List available prompts

# Input Options
--fichier FILES     # Files to process (supports wildcards)
--recursive         # Recursive subdirectory search
--aiall / --auto    # Auto-detect format

# Filtering
--cnbr N           # Process only conversation #N
--only-split       # Only split conversations
--not-split        # Only non-split conversations

# Execution
--simulate         # Test mode (no API calls)
--workers N        # Parallel workers (default: 5)
--delay SECONDS    # Delay between requests (default: 0.5)
--model MODEL      # AI model to use

# Output
--format TYPE      # csv, json, txt, markdown
--output FILE      # Custom output filename
--target-logs DIR  # Logs directory
--target-results DIR # Results directory
```

### Professional Workflow

```bash
#!/bin/bash
# Daily analysis script

DATE=$(date +%Y-%m-%d)
export MISTRAL_API_KEY=$(cat .mistral_key)

./analyse_conversations_merged.py --exec \
  --recursive --aiall \
  --fichier /data/exports/ \
  --prompt-file security_analysis \
  --target-logs "./logs/${DATE}" \
  --target-results "./results/${DATE}" \
  --format markdown \
  --workers 15

# Send notification
echo "Analysis completed: ${DATE}" | mail -s "Report" admin@example.com
```

---

## 🐛 Troubleshooting

### Common Issues

#### "No module named 'X'"
**Solution**: Run installation
```bash
./analyse_conversations_merged.py --install
```

#### "Prompt not found"
**Solution**: Check prompt exists
```bash
./analyse_conversations_merged.py --prompt-list
ls -la prompts/prompt_*.txt
```

#### "API Rate Limit (429)"
**Solution**: Reduce load
```bash
./analyse_conversations_merged.py --exec \
  --workers 3 \
  --delay 1.5 \
  ... other options
```

#### "Permission denied"
**Solution**: Use relative paths
```bash
--target-logs ./logs \
--target-results ./results
```

### Getting Help

```bash
# Basic help
./analyse_conversations_merged.py --help

# Advanced help
./analyse_conversations_merged.py --help-adv

# Version history
./analyse_conversations_merged.py --changelog
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/NoXoZVorteX_prompted.git
cd NoXoZVorteX_prompted
./analyse_conversations_merged.py --install
source .venv_analyse/bin/activate
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Additional Conditions:**
- Any use or modification must retain the original author's name (Bruno DELNOZ) in the credits
- The author remains the primary owner of the project

---

## 👤 Author

**Bruno DELNOZ**
- Email: bruno.delnoz@protonmail.com
- Version: 3.0.2
- Date: October 2025

---

## 🙏 Acknowledgments

- Mistral AI for their powerful API
- The open-source community for inspiration and tools
- All contributors and users of this project

---

## 📞 Support

For questions, issues, or suggestions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review `help_advanced.txt` for detailed documentation
3. Open an issue on GitHub
4. Contact: bruno.delnoz@protonmail.com

---

## 🎯 Roadmap

- [ ] Support for more AI platforms (Gemini, Perplexity)
- [ ] Web UI for easier prompt management
- [ ] Built-in prompt library
- [ ] Database storage for results
- [ ] Real-time progress dashboard
- [ ] Multi-language support

---

**Made with ❤️ by Bruno DELNOZ**
