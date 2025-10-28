#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Results Formatting Module
Handles output in different formats (CSV, JSON, TXT, Markdown)
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class ResultFormatter:
    """Formats and saves results in different formats."""

    @staticmethod
    def save_csv(
        results: List[Dict[str, Any]],
        output_file: str,
        include_metadata: bool = True
    ) -> bool:
        """
        Saves results in CSV format.

        Args:
            results: List of results
            output_file: Output file path
            include_metadata: Include metadata (source file, format, etc.)

        Returns:
            bool: True if success, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                fieldnames = [
                    "conversation_id",
                    "titre_original",
                    "titre",
                    "partie",
                    "response",
                    "success",
                    "error",
                    "token_count"
                ]

                if include_metadata:
                    fieldnames.extend([
                        "fichier_source",
                        "format",
                        "model_used"
                    ])

                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    extrasaction='ignore'
                )
                writer.writeheader()

                # Prepare data
                for r in results:
                    if 'fichier_source' not in r:
                        r['fichier_source'] = r.get('_source_file', 'unknown')
                    if 'format' not in r:
                        r['format'] = r.get('_format', 'unknown')

                writer.writerows(results)

            return True

        except Exception as e:
            print(f"❌ CSV save error: {e}")
            return False

    @staticmethod
    def save_json(
        results: List[Dict[str, Any]],
        output_file: str,
        pretty: bool = True
    ) -> bool:
        """
        Saves results in JSON format.

        Args:
            results: List of results
            output_file: Output file path
            pretty: Format with indentation

        Returns:
            bool: True if success, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(results, f, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"❌ JSON save error: {e}")
            return False

    @staticmethod
    def save_txt(
        results: List[Dict[str, Any]],
        output_file: str,
        separator: str = "\n" + "="*80 + "\n"
    ) -> bool:
        """
        Saves results in simple TXT format.

        Args:
            results: List of results
            output_file: Output file path
            separator: Separator between conversations

        Returns:
            bool: True if success, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("╔" + "═" * 78 + "╗\n")
                f.write("║" + " " * 20 + "ANALYSIS RESULTS" + " " * 42 + "║\n")
                f.write("╚" + "═" * 78 + "╝\n\n")

                f.write(f"Date: {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}\n")
                f.write(f"Number of conversations: {len(results)}\n")
                f.write(f"{'─' * 80}\n\n")

                # Results
                for idx, result in enumerate(results, 1):
                    titre = result.get('titre', 'Untitled')
                    success = result.get('success', False)
                    response = result.get('response', '')
                    error = result.get('error', '')

                    f.write(f"[{idx}] {titre}\n")
                    f.write(f"{'─' * 80}\n")

                    if success:
                        f.write(f"{response}\n")
                    else:
                        f.write(f"❌ ERROR: {error}\n")

                    f.write(separator)

            return True

        except Exception as e:
            print(f"❌ TXT save error: {e}")
            return False

    @staticmethod
    def save_markdown(
        results: List[Dict[str, Any]],
        output_file: str,
        include_toc: bool = True
    ) -> bool:
        """
        Saves results in Markdown format.

        Args:
            results: List of results
            output_file: Output file path
            include_toc: Include table of contents

        Returns:
            bool: True if success, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("# Conversation Analysis Results\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}  \n")
                f.write(f"**Number of conversations**: {len(results)}  \n\n")

                # Quick statistics
                success_count = sum(1 for r in results if r.get('success', False))
                error_count = len(results) - success_count

                f.write("## 📊 Statistics\n\n")
                f.write(f"- ✅ Success: {success_count}\n")
                f.write(f"- ❌ Errors: {error_count}\n\n")
                f.write("---\n\n")

                # Table of contents
                if include_toc:
                    f.write("## 📑 Table of Contents\n\n")
                    for idx, result in enumerate(results, 1):
                        titre = result.get('titre', 'Untitled')
                        anchor = titre.lower().replace(' ', '-')
                        anchor = ''.join(c for c in anchor if c.isalnum() or c == '-')
                        f.write(f"{idx}. [{titre}](#{anchor})\n")
                    f.write("\n---\n\n")

                # Detailed results
                for idx, result in enumerate(results, 1):
                    titre = result.get('titre', 'Untitled')
                    success = result.get('success', False)
                    response = result.get('response', '')
                    error = result.get('error', '')
                    token_count = result.get('token_count', 0)
                    source_file = result.get('_source_file', 'unknown')
                    format_type = result.get('_format', 'unknown')

                    f.write(f"## {idx}. {titre}\n\n")

                    # Metadata
                    f.write(f"**Source**: {source_file}  \n")
                    f.write(f"**Format**: {format_type.upper()}  \n")
                    f.write(f"**Tokens**: {token_count:,}  \n")
                    f.write(f"**Status**: {'✅ Success' if success else '❌ Error'}  \n\n")

                    # Content
                    if success:
                        f.write(f"{response}\n\n")
                    else:
                        f.write(f"**Error**: {error}\n\n")

                    f.write("---\n\n")

            return True

        except Exception as e:
            print(f"❌ Markdown save error: {e}")
            return False
