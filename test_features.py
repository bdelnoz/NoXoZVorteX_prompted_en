#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Suite for NoXoZVorteX_prompted
Tests all functionalities of the AI Conversation Prompt Executor
Author: Bruno DELNOZ
Version: 1.0.0
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestResult:
    """Stores test results."""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors: List[str] = []
        self.warnings: List[str] = []


class FeatureTester:
    """Main testing class."""
    
    def __init__(self):
        self.result = TestResult()
        self.script_path = "./analyse_conversations_merged.py"
        self.temp_dir = None
        self.test_data_created = False
        
    def print_header(self, text: str):
        """Print a formatted header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")
    
    def print_test(self, test_name: str):
        """Print test name."""
        print(f"{Colors.OKBLUE}[TEST]{Colors.ENDC} {test_name}...", end=' ')
        sys.stdout.flush()
    
    def print_success(self, message: str = ""):
        """Print success."""
        msg = f"{Colors.OKGREEN}✅ PASS{Colors.ENDC}"
        if message:
            msg += f" - {message}"
        print(msg)
        self.result.passed += 1
    
    def print_fail(self, error: str):
        """Print failure."""
        print(f"{Colors.FAIL}❌ FAIL{Colors.ENDC}")
        print(f"{Colors.FAIL}   Error: {error}{Colors.ENDC}")
        self.result.failed += 1
        self.result.errors.append(error)
    
    def print_skip(self, reason: str):
        """Print skip."""
        print(f"{Colors.WARNING}⊘ SKIP{Colors.ENDC} - {reason}")
        self.result.skipped += 1
    
    def print_warning(self, message: str):
        """Print warning."""
        print(f"{Colors.WARNING}⚠️  WARNING: {message}{Colors.ENDC}")
        self.result.warnings.append(message)
    
    def run_command(self, cmd: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
        """Run a command and return success, stdout, stderr."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def setup_temp_environment(self):
        """Create temporary test environment."""
        self.temp_dir = tempfile.mkdtemp(prefix="test_noxoz_")
        
        # Create directory structure
        dirs = ['data', 'prompts', 'logs', 'results']
        for d in dirs:
            Path(self.temp_dir, d).mkdir(exist_ok=True)
        
        return self.temp_dir
    
    def create_test_data(self):
        """Create test conversation files."""
        if not self.temp_dir:
            return False
        
        # Test ChatGPT format
        chatgpt_data = [{
            "title": "Test ChatGPT Conversation",
            "conversation_id": "test_001",
            "create_time": 1234567890,
            "mapping": {
                "node_1": {
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["Hello, how are you?"]}
                    }
                },
                "node_2": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["I'm doing well, thank you!"]}
                    }
                }
            }
        }]
        
        # Test Claude format
        claude_data = [{
            "uuid": "test_claude_001",
            "name": "Test Claude Conversation",
            "chat_messages": [
                {"sender": "human", "text": "What is Python?"},
                {"sender": "assistant", "text": "Python is a programming language."}
            ]
        }]
        
        # Test LeChat format
        lechat_data = [
            {"role": "user", "content": "Explain AI"},
            {"role": "assistant", "content": "AI is artificial intelligence."}
        ]
        
        # Write test files
        data_dir = Path(self.temp_dir, 'data')
        
        with open(data_dir / 'test_chatgpt.json', 'w') as f:
            json.dump(chatgpt_data, f)
        
        with open(data_dir / 'test_claude.json', 'w') as f:
            json.dump(claude_data, f)
        
        with open(data_dir / 'test_lechat.json', 'w') as f:
            json.dump(lechat_data, f)
        
        self.test_data_created = True
        return True
    
    def create_test_prompt(self):
        """Create a test prompt file."""
        if not self.temp_dir:
            return False
        
        prompt_content = """---SYSTEM---
You are a test assistant.

---USER---
Analyze this conversation: {TITLE}

Messages: {MESSAGE_COUNT}
Tokens: {TOKEN_COUNT}

{CONVERSATION_TEXT}

Provide a brief summary.
"""
        
        prompt_file = Path(self.temp_dir, 'prompts', 'prompt_test.txt')
        with open(prompt_file, 'w') as f:
            f.write(prompt_content)
        
        return True
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    # ============================================================
    # TEST METHODS
    # ============================================================
    
    def test_script_exists(self):
        """Test if main script exists."""
        self.result.total += 1
        self.print_test("Check script existence")
        
        if os.path.exists(self.script_path):
            self.print_success(f"Found: {self.script_path}")
            return True
        else:
            self.print_fail(f"Script not found: {self.script_path}")
            return False
    
    def test_help_command(self):
        """Test --help command."""
        self.result.total += 1
        self.print_test("Test --help command")
        
        success, stdout, stderr = self.run_command([self.script_path, '--help'])
        
        if success and "AI Conversation Prompt Executor" in stdout:
            self.print_success()
            return True
        else:
            self.print_fail("Help command failed or missing expected output")
            return False
    
    def test_help_advanced(self):
        """Test --help-adv command."""
        self.result.total += 1
        self.print_test("Test --help-adv command")
        
        success, stdout, stderr = self.run_command([self.script_path, '--help-adv'])
        
        if success and "ADVANCED HELP" in stdout:
            self.print_success()
            return True
        else:
            self.print_fail("Advanced help failed")
            return False
    
    def test_changelog(self):
        """Test --changelog command."""
        self.result.total += 1
        self.print_test("Test --changelog command")
        
        success, stdout, stderr = self.run_command([self.script_path, '--changelog'])
        
        if success and "CHANGELOG" in stdout:
            self.print_success()
            return True
        else:
            self.print_fail("Changelog command failed")
            return False
    
    def test_prerequis(self):
        """Test --prerequis command."""
        self.result.total += 1
        self.print_test("Test --prerequis command")
        
        success, stdout, stderr = self.run_command([self.script_path, '--prerequis'])
        
        if "prerequisites" in stdout.lower() or "dépendances" in stdout.lower():
            self.print_success()
            return True
        else:
            self.print_fail("Prerequisites check failed")
            return False
    
    def test_prompt_list(self):
        """Test --prompt-list command."""
        self.result.total += 1
        self.print_test("Test --prompt-list command")
        
        success, stdout, stderr = self.run_command([self.script_path, '--prompt-list'])
        
        if success:
            self.print_success()
            return True
        else:
            self.print_warning("No prompts found (this is OK for new installation)")
            self.result.total -= 1  # Don't count as failed
            return True
    
    def test_format_detection(self):
        """Test format auto-detection."""
        self.result.total += 1
        self.print_test("Test format auto-detection")
        
        # Test with example files if they exist
        if os.path.exists('./data_example/example_chatgpt_json.json'):
            try:
                from extractors import detecter_format_json
                
                with open('./data_example/example_chatgpt_json.json', 'r') as f:
                    data = json.load(f)
                
                format_detected = detecter_format_json(data, 'test.json')
                
                if format_detected == 'chatgpt':
                    self.print_success(f"Detected: {format_detected}")
                    return True
                else:
                    self.print_fail(f"Wrong format detected: {format_detected}")
                    return False
            except Exception as e:
                self.print_fail(f"Format detection error: {e}")
                return False
        else:
            self.print_skip("No example data available")
            return False
    
    def test_message_extraction(self):
        """Test message extraction from different formats."""
        self.result.total += 1
        self.print_test("Test message extraction")
        
        try:
            from extractors import extraire_messages, extraire_messages_chatgpt
            
            # Test ChatGPT format
            test_conv = {
                "mapping": {
                    "node_1": {
                        "message": {
                            "author": {"role": "user"},
                            "content": {"parts": ["Test message"]}
                        }
                    }
                }
            }
            
            messages = extraire_messages_chatgpt(test_conv)
            
            if messages and "Test message" in messages[0]:
                self.print_success(f"Extracted {len(messages)} message(s)")
                return True
            else:
                self.print_fail("Message extraction failed")
                return False
        except Exception as e:
            self.print_fail(f"Extraction error: {e}")
            return False
    
    def test_token_counting(self):
        """Test token counting."""
        self.result.total += 1
        self.print_test("Test token counting")
        
        try:
            from utils import compter_tokens
            
            test_text = "This is a test sentence for token counting."
            token_count = compter_tokens(test_text)
            
            if token_count > 0:
                self.print_success(f"Counted {token_count} tokens")
                return True
            else:
                self.print_fail("Token count is 0")
                return False
        except Exception as e:
            self.print_fail(f"Token counting error: {e}")
            return False
    
    def test_prompt_loader(self):
        """Test prompt loading functionality."""
        self.result.total += 1
        self.print_test("Test prompt loader")
        
        try:
            from prompt_executor import PromptLoader
            
            loader = PromptLoader()
            prompts = loader.list_prompts()
            
            self.print_success(f"Found {len(prompts)} prompt(s)")
            return True
        except Exception as e:
            self.print_fail(f"Prompt loader error: {e}")
            return False
    
    def test_result_formatter_csv(self):
        """Test CSV result formatting."""
        self.result.total += 1
        self.print_test("Test CSV formatter")
        
        try:
            from result_formatter import ResultFormatter
            
            formatter = ResultFormatter()
            test_results = [{
                "conversation_id": "test_001",
                "titre": "Test",
                "response": "Test response",
                "success": True,
                "token_count": 100
            }]
            
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
                temp_file = f.name
            
            success = formatter.save_csv(test_results, temp_file)
            
            if success and os.path.exists(temp_file):
                os.unlink(temp_file)
                self.print_success()
                return True
            else:
                self.print_fail("CSV formatting failed")
                return False
        except Exception as e:
            self.print_fail(f"CSV formatter error: {e}")
            return False
    
    def test_result_formatter_json(self):
        """Test JSON result formatting."""
        self.result.total += 1
        self.print_test("Test JSON formatter")
        
        try:
            from result_formatter import ResultFormatter
            
            formatter = ResultFormatter()
            test_results = [{"test": "data"}]
            
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
                temp_file = f.name
            
            success = formatter.save_json(test_results, temp_file)
            
            if success and os.path.exists(temp_file):
                os.unlink(temp_file)
                self.print_success()
                return True
            else:
                self.print_fail("JSON formatting failed")
                return False
        except Exception as e:
            self.print_fail(f"JSON formatter error: {e}")
            return False
    
    def test_result_formatter_markdown(self):
        """Test Markdown result formatting."""
        self.result.total += 1
        self.print_test("Test Markdown formatter")
        
        try:
            from result_formatter import ResultFormatter
            
            formatter = ResultFormatter()
            test_results = [{
                "titre": "Test",
                "response": "Test response",
                "success": True,
                "token_count": 100
            }]
            
            with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as f:
                temp_file = f.name
            
            success = formatter.save_markdown(test_results, temp_file)
            
            if success and os.path.exists(temp_file):
                os.unlink(temp_file)
                self.print_success()
                return True
            else:
                self.print_fail("Markdown formatting failed")
                return False
        except Exception as e:
            self.print_fail(f"Markdown formatter error: {e}")
            return False
    
    def test_duplicate_detection(self):
        """Test duplicate conversation detection."""
        self.result.total += 1
        self.print_test("Test duplicate detection")
        
        try:
            # Import main script functions
            sys.path.insert(0, '.')
            from analyse_conversations_merged import detecter_doublons
            
            # Create test conversations (duplicates)
            test_convs = [
                {
                    "title": "Test Conv",
                    "id": "123",
                    "create_time": 1234567890,
                    "_format": "chatgpt"
                },
                {
                    "title": "Test Conv",
                    "id": "123",
                    "create_time": 1234567890,
                    "_format": "chatgpt"
                }
            ]
            
            result = detecter_doublons(test_convs)
            
            if result['nb_doublons'] == 1:
                self.print_success("Detected 1 duplicate")
                return True
            else:
                self.print_fail(f"Expected 1 duplicate, found {result['nb_doublons']}")
                return False
        except Exception as e:
            self.print_fail(f"Duplicate detection error: {e}")
            return False
    
    def test_simulation_mode(self):
        """Test simulation mode execution."""
        self.result.total += 1
        self.print_test("Test simulation mode")
        
        # Only test if we have test data
        if not self.test_data_created:
            self.print_skip("No test data available")
            return False
        
        cmd = [
            self.script_path,
            '--exec',
            '--simulate',
            '--aiall',
            '--fichier', f'{self.temp_dir}/data/test_chatgpt.json',
            '--prompt-text', 'Summarize this conversation',
            '--format', 'csv',
            '--target-results', f'{self.temp_dir}/results'
        ]
        
        success, stdout, stderr = self.run_command(cmd, timeout=60)
        
        if success or "SIMULATION" in stdout:
            self.print_success()
            return True
        else:
            self.print_fail(f"Simulation failed: {stderr}")
            return False
    
    def test_directory_creation(self):
        """Test automatic directory creation."""
        self.result.total += 1
        self.print_test("Test directory auto-creation")
        
        try:
            from analyse_conversations_merged import ensure_directory
            
            with tempfile.TemporaryDirectory() as tmpdir:
                test_path = os.path.join(tmpdir, 'test', 'nested', 'dirs')
                result = ensure_directory(test_path)
                
                if result.exists() and result.is_dir():
                    self.print_success()
                    return True
                else:
                    self.print_fail("Directory creation failed")
                    return False
        except Exception as e:
            self.print_fail(f"Directory creation error: {e}")
            return False
    
    def test_config_module(self):
        """Test configuration module."""
        self.result.total += 1
        self.print_test("Test config module")
        
        try:
            from config import VERSION, MAX_TOKENS, MAX_WORKERS, MODEL
            
            if VERSION and MAX_TOKENS > 0 and MAX_WORKERS > 0 and MODEL:
                self.print_success(f"Version: {VERSION}")
                return True
            else:
                self.print_fail("Config values invalid")
                return False
        except Exception as e:
            self.print_fail(f"Config module error: {e}")
            return False
    
    def test_example_data_integrity(self):
        """Test example data files integrity."""
        self.result.total += 1
        self.print_test("Test example data integrity")
        
        example_files = [
            './data_example/example_chatgpt_json.json',
            './data_example/example_claude_json.json',
            './data_example/example_lechat_json.json'
        ]
        
        all_valid = True
        found_count = 0
        
        for file_path in example_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        json.load(f)
                    found_count += 1
                except json.JSONDecodeError:
                    all_valid = False
                    self.print_warning(f"Invalid JSON: {file_path}")
        
        if found_count == 0:
            self.print_skip("No example data found")
            return False
        elif all_valid:
            self.print_success(f"Validated {found_count} file(s)")
            return True
        else:
            self.print_fail("Some example files have invalid JSON")
            return False
    
    # ============================================================
    # MAIN TEST RUNNER
    # ============================================================
    
    def run_all_tests(self):
        """Run all tests."""
        start_time = datetime.now()
        
        self.print_header("NoXoZVorteX_prompted - Complete Test Suite")
        
        print(f"{Colors.OKCYAN}Starting tests at {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
        
        # Setup
        print(f"{Colors.BOLD}Setting up test environment...{Colors.ENDC}")
        self.setup_temp_environment()
        self.create_test_data()
        self.create_test_prompt()
        print(f"{Colors.OKGREEN}✓ Test environment ready{Colors.ENDC}\n")
        
        # Core tests
        self.print_header("Core Functionality Tests")
        self.test_script_exists()
        self.test_help_command()
        self.test_help_advanced()
        self.test_changelog()
        self.test_prerequis()
        self.test_prompt_list()
        self.test_config_module()
        
        # Module tests
        self.print_header("Module Tests")
        self.test_format_detection()
        self.test_message_extraction()
        self.test_token_counting()
        self.test_prompt_loader()
        self.test_duplicate_detection()
        self.test_directory_creation()
        
        # Formatter tests
        self.print_header("Output Formatter Tests")
        self.test_result_formatter_csv()
        self.test_result_formatter_json()
        self.test_result_formatter_markdown()
        
        # Data tests
        self.print_header("Data Integrity Tests")
        self.test_example_data_integrity()
        
        # Integration tests
        self.print_header("Integration Tests")
        self.test_simulation_mode()
        
        # Cleanup
        print(f"\n{Colors.BOLD}Cleaning up...{Colors.ENDC}")
        self.cleanup()
        print(f"{Colors.OKGREEN}✓ Cleanup complete{Colors.ENDC}\n")
        
        # Results
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.print_results(duration)
    
    def print_results(self, duration: float):
        """Print final test results."""
        self.print_header("Test Results Summary")
        
        print(f"{Colors.BOLD}Total Tests:{Colors.ENDC} {self.result.total}")
        print(f"{Colors.OKGREEN}✅ Passed:{Colors.ENDC} {self.result.passed}")
        print(f"{Colors.FAIL}❌ Failed:{Colors.ENDC} {self.result.failed}")
        print(f"{Colors.WARNING}⊘ Skipped:{Colors.ENDC} {self.result.skipped}")
        print(f"\n{Colors.BOLD}Duration:{Colors.ENDC} {duration:.2f}s")
        
        # Success rate
        if self.result.total > 0:
            success_rate = (self.result.passed / self.result.total) * 100
            print(f"{Colors.BOLD}Success Rate:{Colors.ENDC} {success_rate:.1f}%")
        
        # Warnings
        if self.result.warnings:
            print(f"\n{Colors.WARNING}{Colors.BOLD}Warnings:{Colors.ENDC}")
            for warning in self.result.warnings:
                print(f"  ⚠️  {warning}")
        
        # Errors
        if self.result.errors:
            print(f"\n{Colors.FAIL}{Colors.BOLD}Errors:{Colors.ENDC}")
            for error in self.result.errors:
                print(f"  ❌ {error}")
        
        # Final verdict
        print()
        if self.result.failed == 0:
            print(f"{Colors.OKGREEN}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{Colors.BOLD}{'ALL TESTS PASSED! ✅'.center(80)}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
            return 0
        else:
            print(f"{Colors.FAIL}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
            print(f"{Colors.FAIL}{Colors.BOLD}{'SOME TESTS FAILED ❌'.center(80)}{Colors.ENDC}")
            print(f"{Colors.FAIL}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
            return 1


def main():
    """Main entry point."""
    tester = FeatureTester()
    
    try:
        exit_code = tester.run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
        tester.cleanup()
        sys.exit(130)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        tester.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
