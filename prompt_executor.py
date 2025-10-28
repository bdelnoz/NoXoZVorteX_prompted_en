#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom Prompt Execution Module
Handles loading, formatting and execution of prompts via Mistral API
"""

import os
import time
import random
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path


def ensure_directory(directory: str) -> Path:
    """
    Ensures a directory exists, creates it if necessary.

    Args:
        directory: Directory path

    Returns:
        Path: Path object of created directory
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


class PromptLoader:
    """Loads and manages prompt files."""

    def __init__(self, prompt_dir: str = "prompts"):
        self.prompt_dir = Path(prompt_dir)
        self.prompt_dir.mkdir(exist_ok=True)

    def list_prompts(self) -> List[str]:
        """Lists all available prompts."""
        if not self.prompt_dir.exists():
            return []

        prompts = []
        for file in self.prompt_dir.glob("prompt_*.txt"):
            # Remove "prompt_" prefix and ".txt" extension
            prompt_name = file.stem.replace("prompt_", "")
            prompts.append(prompt_name)
        return sorted(prompts)

    def load_prompt(self, prompt_name: str) -> Optional[str]:
        """Loads a prompt file."""
        # Automatically add prefix if missing
        if not prompt_name.startswith("prompt_"):
            prompt_name = f"prompt_{prompt_name}"

        prompt_path = self.prompt_dir / f"{prompt_name}.txt"

        if not prompt_path.exists():
            return None

        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading prompt {prompt_name}: {e}")
            return None

    def load_prompt_from_file(self, file_path: str) -> Optional[str]:
        """Loads a prompt from a file path."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None


class PromptFormatter:
    """Formats prompts with conversation variables."""

    @staticmethod
    def format_prompt(
        template: str,
        conversation: Dict[str, Any],
        messages: List[str]
    ) -> str:
        """
        Replaces variables in the prompt template.

        Available variables:
        - {CONVERSATION_TEXT}: Complete text
        - {TITLE}: Title
        - {MESSAGE_COUNT}: Number of messages
        - {TOKEN_COUNT}: Number of tokens
        - {FORMAT}: Source format
        - {FILE}: Source file
        """
        conversation_text = "\n\n".join(messages)

        variables = {
            'CONVERSATION_TEXT': conversation_text,
            'TITLE': conversation.get('title', 'Untitled'),
            'MESSAGE_COUNT': str(len(messages)),
            'TOKEN_COUNT': str(conversation.get('token_count', 0)),
            'FORMAT': conversation.get('_format', 'unknown').upper(),
            'FILE': conversation.get('_source_file', 'unknown')
        }

        # Variable replacement
        formatted = template
        for key, value in variables.items():
            formatted = formatted.replace(f"{{{key}}}", value)

        return formatted

    @staticmethod
    def parse_system_user(prompt: str) -> tuple:
        """
        Separates prompt into SYSTEM and USER parts if present.

        Syntax:
        ---SYSTEM---
        System instructions
        ---USER---
        User prompt
        """
        if '---SYSTEM---' in prompt and '---USER---' in prompt:
            parts = prompt.split('---SYSTEM---', 1)[1]
            system_part, user_part = parts.split('---USER---', 1)
            return system_part.strip(), user_part.strip()

        # Default: everything is user prompt
        return None, prompt.strip()


class PromptExecutor:
    """Executes prompts via API."""

    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.mistral.ai/v1/chat/completions",
        model: str = "pixtral-large-latest"
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def execute_prompt(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16000,
        simulate: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a prompt via API.

        Returns:
            {
                'success': bool,
                'response': str,
                'error': str (if failed)
            }
        """
        if simulate:
            time.sleep(random.uniform(0.1, 0.3))
            return {
                'success': True,
                'response': '[SIMULATION] Simulated model response',
                'simulate': True
            }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []

        # Add system prompt if present
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add user prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()

                result = response.json()
                content = result["choices"][0]["message"]["content"]

                return {
                    'success': True,
                    'response': content,
                    'model': self.model,
                    'tokens_used': result.get('usage', {})
                }

            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else "Unknown"

                if attempt < max_retries - 1 and (status_code == 429 or status_code >= 500):
                    wait_time = 5 * (2 ** attempt) if status_code == 429 else (attempt + 1) * 2
                    time.sleep(wait_time)
                    continue

                return {
                    'success': False,
                    'error': f"HTTP {status_code}: {str(e)}"
                }

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue

                return {
                    'success': False,
                    'error': "Timeout after multiple attempts"
                }

            except Exception as e:
                return {
                    'success': False,
                    'error': f"{type(e).__name__}: {str(e)}"
                }

        return {
            'success': False,
            'error': "Failed after all retries"
        }


def process_conversation_with_prompt(
    conversation: Dict[str, Any],
    messages: List[str],
    prompt_template: str,
    executor: PromptExecutor,
    simulate: bool = False,
    delay: float = 0.5
) -> Dict[str, Any]:
    """
    Processes a conversation with a custom prompt.

    Returns:
        {
            'conversation_id': str,
            'titre': str,
            'response': str,
            'success': bool,
            'error': str (if failed),
            'token_count': int,
            'partie': str
        }
    """
    titre = conversation.get("title", "Untitled")

    base_result = {
        "conversation_id": conversation.get("conversation_id", ""),
        "titre_original": conversation.get("titre_original", titre),
        "titre": titre,
        "partie": conversation.get("partie", "1/1"),
        "_source_file": conversation.get("_source_file", "unknown"),
        "_format": conversation.get("_format", "unknown")
    }

    if not messages:
        return {
            **base_result,
            "success": False,
            "response": "",
            "error": "No messages",
            "token_count": 0
        }

    # Calculate tokens
    from utils import compter_tokens
    conversation_text = "\n".join(messages)
    token_count = compter_tokens(conversation_text)

    # Add token_count to conversation for formatter
    conversation['token_count'] = token_count

    # Format prompt
    formatter = PromptFormatter()
    formatted_prompt = formatter.format_prompt(prompt_template, conversation, messages)

    # Separate system/user if present
    system_prompt, user_prompt = formatter.parse_system_user(formatted_prompt)

    # Delay between requests
    if not simulate:
        time.sleep(delay)

    # Execute prompt
    result = executor.execute_prompt(
        user_prompt,
        system_prompt=system_prompt,
        simulate=simulate
    )

    return {
        **base_result,
        "success": result['success'],
        "response": result.get('response', ''),
        "error": result.get('error', ''),
        "token_count": token_count,
        "model_used": result.get('model', ''),
        "tokens_used": result.get('tokens_used', {})
    }


# ============================================
# UTILITY FUNCTIONS
# ============================================

def create_default_prompts(prompt_dir: str = "prompts"):
    """Creates default example prompts."""
    prompt_path = Path(prompt_dir)
    prompt_path.mkdir(exist_ok=True)

    default_prompts = {
        "prompt_resume.txt": """You are an expert in conversation summarization.

Analyze this conversation and provide a structured summary.

Conversation:
{CONVERSATION_TEXT}

Expected format:
1. Summary in 3 key points
2. Main topics discussed
3. Important conclusions or decisions

Be concise and factual.""",

        "prompt_extract_topics.txt": """You are a content analyst.

Extract the main topics from this conversation.

Conversation:
{CONVERSATION_TEXT}

List only the topics, one per line, without numbering.""",

        "prompt_questions.txt": """You are an analysis assistant.

Identify in this conversation:
1. Questions asked by the user
2. Questions that need follow-up

Conversation:
{CONVERSATION_TEXT}

Format: bulleted list."""
    }

    created = []
    for filename, content in default_prompts.items():
        file_path = prompt_path / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created.append(filename)

    return created
