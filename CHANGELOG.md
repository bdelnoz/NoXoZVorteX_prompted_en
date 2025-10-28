# Changelog

All notable changes to the NoXoZVorteX_prompted project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.2] - 2025-10-28

### Fixed
- Log file path resolution for `--target-logs` directory
- Report generation file path consistency
- Improved error handling in file operations

### Changed
- Enhanced logging system with proper directory handling
- Improved file report generation with correct paths

---

## [3.0.0] - 2025-10-26 - MAJOR REFACTORING

### Added ⭐
- **Customizable prompt system** via `prompt_*.txt` files
- `--prompt-file`: Use prompt files from `prompts/` directory
- `--prompt-list`: List all available prompts
- `--prompt-text`: Execute direct inline prompts
- `--help-adv`: Complete advanced help from `help_advanced.txt`
- `--target-logs`: Custom directory for logs
- `--target-results`: Custom directory for results
- `--format`: Multiple output formats (csv, json, txt, markdown)
- **Automatic duplicate detection and elimination** using hash-based comparison
- **Variables in prompts**: `{CONVERSATION_TEXT}`, `{TITLE}`, `{MESSAGE_COUNT}`, etc.
- **SYSTEM/USER prompt support** with `---SYSTEM---` / `---USER---` syntax
- Automatic folder creation (mkdir -p equivalent)
- `prompt_executor.py` module: Complete prompt management
- `result_formatter.py` module: Multiple output formats
- Complete `STRUCTURE.md` documentation
- Example prompts for security analysis and child safety

### Changed
- Simplified architecture: 8 files instead of 12
- Removed `--local` mode (API-only now)
- Enhanced file organization with custom directories
- Improved error messages and user feedback
- Better handling of long conversations with automatic splitting

### Removed
- Local analysis mode (now API-only)
- Legacy analysis methods
- Deprecated configuration options

---

## [2.7.5] - 2025-10-22

### Fixed
- Import error in `verifier_prerequis` function
- Logic correction in prerequisite verification

---

## [2.7.0] - 2025-10-19

### Added
- Automatic TXT file generation with all analyzed topics
- Ultra-complete operations report
- Visual split indicator (✂️/✅) in reports
- Execution time and performance metrics
- Total disk space calculation for generated files

### Changed
- Enhanced report formatting with more statistics
- Improved visual feedback during processing

---

## [2.6.0] - 2025-10-19

### Added
- Complete operations report after analysis
- Detailed split vs non-split statistics
- File summary table in reports

### Changed
- Improved report generation with better statistics
- Enhanced visual presentation of results

---

## [2.5.0] - 2025-10-19

### Added
- **Multi-format auto-detection** for ChatGPT, Claude, and LeChat
- Simultaneous support for multiple AI conversation formats
- Reinforced AI focus with 3x scoring weight
- Support for 35+ skill domains
- Complete logging system with rotation

### Changed
- Enhanced format detection algorithm
- Improved conversation parsing for all formats
- Better error handling for malformed JSON

---

## [2.4.0] - 2025-10-19

### Added
- **MULTI-FORMAT AUTO-DETECTION** capability
- `--aiall` flag: Process all AI formats automatically
- Smart format recognition for mixed conversation exports

### Changed
- Enhanced conversation loading with format detection
- Improved compatibility across different AI platforms

---

## [2.3.0] - 2025-10-18

### Added
- Maximum priority on AI/ML skills detection
- Exhaustive AI technology recognition
- Automatic categorization of conversations by topic

### Changed
- Refined skill detection algorithms
- Enhanced topic extraction for AI-related conversations
- Improved scoring system for technical content

---

## [2.2.0] - 2025-10-17

### Added
- Parallel processing with `ThreadPoolExecutor`
- `--workers` flag for concurrent API requests
- Progress bar with `tqdm` integration
- Enhanced performance for large datasets

### Changed
- Significantly improved processing speed
- Better resource utilization
- Optimized API call management

---

## [2.1.0] - 2025-10-16

### Added
- Support for Claude conversation format
- `--claude` flag for Claude-specific parsing
- Extended format detection

### Changed
- Enhanced message extraction for different formats
- Improved conversation metadata handling

---

## [2.0.0] - 2025-10-15 - MAJOR UPDATE

### Added
- Support for LeChat (Mistral) conversation format
- `--lechat` flag for Mistral-specific parsing
- Unified conversation processing pipeline
- Enhanced error handling and logging

### Changed
- Refactored conversation extraction logic
- Improved modularity with separate `extractors.py`
- Better separation of concerns

---

## [1.5.0] - 2025-10-10

### Added
- CSV output format support
- `--output` flag for custom filenames
- Basic filtering options (`--cnbr`, `--only-split`, `--not-split`)

### Changed
- Enhanced output formatting
- Improved file naming conventions

---

## [1.0.0] - 2025-10-01 - INITIAL RELEASE

### Added
- Basic ChatGPT conversation analysis
- Topic extraction functionality
- Mistral API integration
- Virtual environment management
- Installation and prerequisite checking
- Basic logging system
- Command-line interface

---

## Version History Summary

- **v3.x**: Custom prompts, multi-format output, enhanced UX
- **v2.x**: Multi-AI support, parallel processing, auto-detection
- **v1.x**: Initial release with ChatGPT support

---

## Upgrade Guide

### From 2.x to 3.x

**Breaking Changes:**
- `--local` mode removed (use `--simulate` for testing)
- Old analysis methods deprecated (use custom prompts)

**Migration Steps:**
1. Create custom prompts in `prompts/` directory
2. Replace `--local` with `--simulate` for testing
3. Update output paths to use `--target-results` and `--target-logs`
4. Review new `--format` options (csv, json, txt, markdown)

**Example:**
```bash
# Old (v2.x)
python script.py --exec --local --fichier data.json

# New (v3.x)
python analyse_conversations_merged.py --exec \
  --prompt-file my_analysis \
  --fichier data.json \
  --format markdown
```

---

## Future Plans

### Planned for v3.1.0
- [ ] Add support for Gemini conversations
- [ ] Web UI for prompt management
- [ ] Built-in prompt library
- [ ] Real-time progress dashboard

### Planned for v4.0.0
- [ ] Database storage for results
- [ ] Multi-language support
- [ ] Plugin system for custom analyzers
- [ ] RESTful API for remote analysis

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this changelog and the project.

---

## Authors

- **Bruno DELNOZ** - *Initial work and ongoing maintenance* - [bruno.delnoz@protonmail.com](mailto:bruno.delnoz@protonmail.com)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
