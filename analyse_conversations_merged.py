#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script name: analyse_conversations_merged.py
Author: Bruno DELNOZ - bruno.delnoz@protonmail.com
Version: v3.0.2 - LOG AND REPORT FIXES
Date: 2025-10-28

Main script - Custom prompt execution engine
"""

import os
import sys
import argparse
import json
import csv
import glob
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Local module imports
from config import (
    VERSION, MAX_WORKERS, MODEL, MAX_TOKENS,
    ENV_DIR, obtenir_api_key
)
from utils import compter_tokens
from extractors import extraire_messages, detecter_format_json
from install import (
    verifier_prerequis_complet, verifier_dependances, installer_dependances,
    supprimer_fichier
)
from help import afficher_aide, afficher_aide_avancee, afficher_changelog

# Global variables for directories
LOGS_DIR = None
RESULTS_DIR = None


def ecrire_log_local(message: str, niveau: str = "INFO") -> None:
    """Writes to log file with the correct directory."""
    if LOGS_DIR is None:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{niveau}] {message}\n"

    try:
        log_file = LOGS_DIR / f"log.prompt_executor.{VERSION}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
    except Exception as e:
        print(f"⚠️ Log error: {e}")


def ensure_directory(directory: str) -> Path:
    """
    Ensures a directory exists, creates it if necessary.

    Args:
        directory: Directory path

    Returns:
        Path: Path object of created directory
    """
    dir_path = Path(directory).resolve()
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def generer_hash_conversation(conv: Dict, format_conv: str) -> str:
    """Generates a unique hash to detect duplicates."""
    signature_parts = []

    titre = conv.get("title", conv.get("name", ""))
    if titre:
        signature_parts.append(f"title:{titre}")

    conv_id = conv.get("id", conv.get("uuid", conv.get("conversation_id", "")))
    if conv_id:
        signature_parts.append(f"id:{conv_id}")

    created = conv.get("create_time", conv.get("created_at", conv.get("createdAt", "")))
    if created:
        signature_parts.append(f"created:{created}")

    if format_conv == "chatgpt":
        mapping = conv.get("mapping", {})
        nb_messages = len([m for m in mapping.values() if m.get("message")])
    elif format_conv == "lechat":
        messages = conv.get("messages", conv.get("exchanges", []))
        nb_messages = len(messages)
    elif format_conv == "claude":
        messages = conv.get("chat_messages", [])
        nb_messages = len(messages)
    else:
        nb_messages = 0

    signature_parts.append(f"msgs:{nb_messages}")

    signature = "|".join(signature_parts)
    return hashlib.sha256(signature.encode('utf-8')).hexdigest()


def detecter_doublons(toutes_conversations: List[Dict]) -> Dict[str, Any]:
    """Detects duplicate conversations."""
    hash_map = {}
    doublons = []
    conversations_uniques = []

    for idx, conv in enumerate(toutes_conversations):
        format_conv = conv.get('_format', 'unknown')
        conv_hash = generer_hash_conversation(conv, format_conv)

        if conv_hash in hash_map:
            original_idx = hash_map[conv_hash]
            original_conv = toutes_conversations[original_idx]

            doublons.append({
                'original': {
                    'index': original_idx,
                    'titre': original_conv.get('title', original_conv.get('name', 'Untitled')),
                    'fichier': original_conv.get('_source_file', 'unknown'),
                    'format': original_conv.get('_format', 'unknown')
                },
                'doublon': {
                    'index': idx,
                    'titre': conv.get('title', conv.get('name', 'Untitled')),
                    'fichier': conv.get('_source_file', 'unknown'),
                    'format': conv.get('_format', 'unknown')
                },
                'hash': conv_hash
            })
        else:
            hash_map[conv_hash] = idx
            conversations_uniques.append(conv)

    return {
        'conversations_uniques': conversations_uniques,
        'doublons': doublons,
        'nb_total': len(toutes_conversations),
        'nb_uniques': len(conversations_uniques),
        'nb_doublons': len(doublons)
    }


def charger_fichiers(fichiers_a_traiter: List[str], format_source: str) -> tuple:
    """Loads and analyzes JSON files."""
    toutes_conversations = []
    stats_chargement = {'chatgpt': 0, 'lechat': 0, 'claude': 0, 'unknown': 0, 'erreurs': 0}
    details_fichiers = []  # For detailed report

    print("📂 Loading files...")
    ecrire_log_local("=== FILE LOADING START ===", "INFO")

    for fichier in fichiers_a_traiter:
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            if format_source == "auto":
                format_detecte = detecter_format_json(data, fichier)
            else:
                format_detecte = format_source

            stats_chargement[format_detecte] = stats_chargement.get(format_detecte, 0) + 1
            nb_conv = 0
            nb_messages_total = 0
            titres_conversations = []

            if format_detecte == "chatgpt":
                if isinstance(data, list):
                    nb_conv = len(data)
                    for conv in data:
                        conv['_source_file'] = os.path.basename(fichier)
                        conv['_format'] = 'chatgpt'
                        titre = conv.get('title', 'Untitled')
                        titres_conversations.append(titre)

                        # Count messages
                        mapping = conv.get('mapping', {})
                        nb_messages_total += len([m for m in mapping.values() if m.get('message')])

                        toutes_conversations.append(conv)

                    msg = f"✅ ChatGPT: {os.path.basename(fichier)} ({nb_conv} conversations, {nb_messages_total} messages)"
                    print(f"   {msg}")
                    ecrire_log_local(msg, "INFO")

            elif format_detecte == "lechat":
                if isinstance(data, list):
                    nb_conv = 1
                    nb_messages_total = len(data)
                    titre = os.path.splitext(os.path.basename(fichier))[0]
                    import re
                    titre = re.sub(r'^chat-', '', titre)
                    titre = re.sub(r'^AI_exportation_', '', titre)
                    titre = re.sub(r'_conversations$', '', titre)
                    titres_conversations.append(titre)

                    conv = {
                        "title": titre or "LeChat Conversation",
                        "messages": data,
                        "_source_file": os.path.basename(fichier),
                        "_format": "lechat"
                    }
                    toutes_conversations.append(conv)

                    msg = f"✅ LeChat: {os.path.basename(fichier)} ({nb_messages_total} messages)"
                    print(f"   {msg}")
                    ecrire_log_local(msg, "INFO")

                elif isinstance(data, dict):
                    nb_conv = 1
                    titre = data.get("title", os.path.splitext(os.path.basename(fichier))[0])
                    titres_conversations.append(titre)
                    data['title'] = titre
                    data['_source_file'] = os.path.basename(fichier)
                    data['_format'] = 'lechat'
                    toutes_conversations.append(data)
                    nb_messages_total = len(data.get('messages', data.get('exchanges', [])))

                    msg = f"✅ LeChat: {os.path.basename(fichier)} ({nb_messages_total} messages)"
                    print(f"   {msg}")
                    ecrire_log_local(msg, "INFO")

            elif format_detecte == "claude":
                if isinstance(data, list):
                    nb_conv = len(data)
                    for conv in data:
                        conv['_source_file'] = os.path.basename(fichier)
                        conv['_format'] = 'claude'
                        if 'title' not in conv and 'name' not in conv:
                            conv['title'] = f"Claude - {conv.get('uuid', 'Untitled')[:8]}"

                        titre = conv.get('title', conv.get('name', 'Untitled'))
                        titres_conversations.append(titre)

                        # Count messages
                        chat_messages = conv.get('chat_messages', [])
                        nb_messages_total += len(chat_messages)

                        toutes_conversations.append(conv)

                    msg = f"✅ Claude: {os.path.basename(fichier)} ({nb_conv} conversations, {nb_messages_total} messages)"
                    print(f"   {msg}")
                    ecrire_log_local(msg, "INFO")

                elif isinstance(data, dict):
                    nb_conv = 1
                    data['_source_file'] = os.path.basename(fichier)
                    data['_format'] = 'claude'
                    if 'title' not in data and 'name' not in data:
                        data['title'] = f"Claude - {data.get('uuid', 'Untitled')[:8]}"

                    titre = data.get('title', data.get('name', 'Untitled'))
                    titres_conversations.append(titre)
                    chat_messages = data.get('chat_messages', [])
                    nb_messages_total = len(chat_messages)

                    toutes_conversations.append(data)

                    msg = f"✅ Claude: {os.path.basename(fichier)} ({nb_messages_total} messages)"
                    print(f"   {msg}")
                    ecrire_log_local(msg, "INFO")

            else:
                msg = f"⚠️ Unknown format: {os.path.basename(fichier)}"
                print(f"   {msg}")
                ecrire_log_local(msg, "WARNING")
                stats_chargement['unknown'] = stats_chargement.get('unknown', 0) + 1

            # Save details for report
            details_fichiers.append({
                'fichier': os.path.basename(fichier),
                'chemin_complet': fichier,
                'format': format_detecte.upper(),
                'nb_conversations': nb_conv,
                'nb_messages': nb_messages_total,
                'titres': titres_conversations,
                'statut': 'OK'
            })

            # Log each conversation title
            if titres_conversations:
                ecrire_log_local(f"  Conversations in {os.path.basename(fichier)}:", "INFO")
                for idx, titre in enumerate(titres_conversations, 1):
                    ecrire_log_local(f"    [{idx}] {titre}", "INFO")

        except json.JSONDecodeError as e:
            msg = f"❌ JSON error: {os.path.basename(fichier)}"
            print(f"   {msg}")
            ecrire_log_local(f"JSON error {fichier}: {e}", "ERROR")
            stats_chargement['erreurs'] += 1

            details_fichiers.append({
                'fichier': os.path.basename(fichier),
                'chemin_complet': fichier,
                'format': 'ERROR',
                'nb_conversations': 0,
                'nb_messages': 0,
                'titres': [],
                'statut': f'ERROR: {str(e)[:100]}'
            })

        except Exception as e:
            msg = f"❌ Error: {os.path.basename(fichier)}"
            print(f"   {msg}")
            ecrire_log_local(f"Error {fichier}: {e}", "ERROR")
            stats_chargement['erreurs'] += 1

            details_fichiers.append({
                'fichier': os.path.basename(fichier),
                'chemin_complet': fichier,
                'format': 'ERROR',
                'nb_conversations': 0,
                'nb_messages': 0,
                'titres': [],
                'statut': f'ERROR: {str(e)[:100]}'
            })

    ecrire_log_local("=== FILE LOADING END ===", "INFO")

    return toutes_conversations, stats_chargement, details_fichiers


# CONTINUATION OF analyse_conversations_merged.py

def generer_rapport_fichiers(details_fichiers: List[Dict], logs_dir: Path) -> None:
    """Generates a detailed report of loaded files."""
    rapport_file = logs_dir / f"files_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        with open(rapport_file, 'w', encoding='utf-8') as f:
            f.write("╔" + "═" * 78 + "╗\n")
            f.write("║" + " " * 20 + "FILE LOADING REPORT" + " " * 39 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n\n")

            f.write(f"Date: {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}\n")
            f.write(f"Number of files processed: {len(details_fichiers)}\n\n")

            f.write("=" * 80 + "\n")
            f.write("DETAILS BY FILE\n")
            f.write("=" * 80 + "\n\n")

            for idx, detail in enumerate(details_fichiers, 1):
                f.write(f"[{idx}] {detail['fichier']}\n")
                f.write(f"    Path: {detail['chemin_complet']}\n")
                f.write(f"    Format: {detail['format']}\n")
                f.write(f"    Status: {detail['statut']}\n")
                f.write(f"    Conversations: {detail['nb_conversations']}\n")
                f.write(f"    Messages: {detail['nb_messages']}\n")

                if detail['titres']:
                    f.write(f"    Conversation titles:\n")
                    for titre_idx, titre in enumerate(detail['titres'], 1):
                        f.write(f"        [{titre_idx}] {titre}\n")

                f.write("\n" + "-" * 80 + "\n\n")

            # Statistics by format
            f.write("=" * 80 + "\n")
            f.write("STATISTICS BY AI FORMAT\n")
            f.write("=" * 80 + "\n\n")

            formats_stats = {}
            for detail in details_fichiers:
                fmt = detail['format']
                if fmt not in formats_stats:
                    formats_stats[fmt] = {'fichiers': 0, 'conversations': 0, 'messages': 0}
                formats_stats[fmt]['fichiers'] += 1
                formats_stats[fmt]['conversations'] += detail['nb_conversations']
                formats_stats[fmt]['messages'] += detail['nb_messages']

            for fmt, stats in sorted(formats_stats.items()):
                f.write(f"{fmt}:\n")
                f.write(f"  Files: {stats['fichiers']}\n")
                f.write(f"  Conversations: {stats['conversations']}\n")
                f.write(f"  Messages: {stats['messages']}\n\n")

        print(f"📄 Files report generated: {rapport_file}")
        ecrire_log_local(f"Files report generated: {rapport_file}", "INFO")

    except Exception as e:
        print(f"⚠️ Report generation error: {e}")
        ecrire_log_local(f"Report generation error: {e}", "ERROR")


def decouper_conversation(conversation: Dict[str, Any], messages: List[str]) -> List[Dict[str, Any]]:
    """Splits a conversation if > MAX_TOKENS."""
    import uuid

    titre = conversation.get("title", "Untitled")

    if not messages:
        return [{"title": titre, "messages": [], "partie": "1/1"}]

    texte_complet = "\n".join(messages)
    token_count = compter_tokens(texte_complet)

    if token_count <= MAX_TOKENS:
        return [{
            "title": titre,
            "messages": messages,
            "partie": "1/1",
            "titre_original": titre
        }]

    conv_id = str(uuid.uuid4())
    moitie = len(messages) // 2

    return [
        {
            "title": f"{titre} (Part 1/2)",
            "messages": messages[:moitie],
            "conversation_id": conv_id,
            "partie": "1/2",
            "titre_original": titre
        },
        {
            "title": f"{titre} (Part 2/2)",
            "messages": messages[moitie:],
            "conversation_id": conv_id,
            "partie": "2/2",
            "titre_original": titre
        }
    ]


def main() -> None:
    """Main function."""
    global LOGS_DIR, RESULTS_DIR

    temps_debut = time.time()

    if len(sys.argv) == 1:
        afficher_aide()
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    parser.add_argument('--help-adv', action='store_true')
    parser.add_argument('--exec', action='store_true')
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--chatgpt', action='store_true', default=False)
    parser.add_argument('--lechat', action='store_true', default=False)
    parser.add_argument('--claude', action='store_true', default=False)
    parser.add_argument('--aiall', '--auto', action='store_true', default=False)
    parser.add_argument('--simulate', action='store_true', default=False)
    parser.add_argument('--only-split', action='store_true', default=False)
    parser.add_argument('--not-split', action='store_true', default=False)
    parser.add_argument('--cnbr', type=int)
    parser.add_argument('--fichier', '-F', type=str, nargs='*', default=[])
    parser.add_argument('--model', '-m', type=str, default=MODEL)
    parser.add_argument('--workers', '-w', type=int, default=MAX_WORKERS)
    parser.add_argument('--delay', '-d', type=float, default=0.5)
    parser.add_argument('--prerequis', action='store_true')
    parser.add_argument('--changelog', action='store_true')
    parser.add_argument('--recursive', action='store_true', default=False)

    # New arguments v3.0
    parser.add_argument('--prompt-file', '-p', type=str)
    parser.add_argument('--prompt-list', action='store_true')
    parser.add_argument('--prompt-text', '-pt', type=str)
    parser.add_argument('--format', choices=['csv', 'json', 'txt', 'markdown'], default='csv')
    parser.add_argument('--output', '-o', type=str)
    parser.add_argument('--target-logs', type=str, default='./')
    parser.add_argument('--target-results', type=str, default='./')

    args = parser.parse_args()

    # Handle simple commands
    if args.help:
        afficher_aide()
        return

    if args.help_adv:
        afficher_aide_avancee()
        return

    if args.changelog:
        afficher_changelog()
        return

    if args.prerequis:
        verifier_prerequis_complet()
        return

    if args.install:
        installer_dependances()
        return

    if args.prompt_list:
        from prompt_executor import PromptLoader
        loader = PromptLoader()
        prompts = loader.list_prompts()
        if prompts:
            print("\n📋 Available prompts:\n")
            for i, p in enumerate(prompts, 1):
                print(f"   {i}. {p}")
            print()
        else:
            print("\n⚠️  No prompts found in 'prompts/' folder\n")
        return

    if not args.exec:
        print("❌ Use --exec to launch the analysis.")
        print("💡 Use --help or --help-adv for more information.")
        return

    # Prompt verification
    if not args.prompt_file and not args.prompt_text:
        print("❌ You must specify a prompt:")
        print("   --prompt-file <prompt_name>")
        print("   OR")
        print("   --prompt-text \"your prompt\"")
        print("\n💡 Use --prompt-list to see available prompts")
        return

    # Create output directories
    LOGS_DIR = ensure_directory(args.target_logs)
    RESULTS_DIR = ensure_directory(args.target_results)

    # Initialize log
    ecrire_log_local("=" * 80, "INFO")
    ecrire_log_local("CONVERSATION ANALYSIS START", "INFO")
    ecrire_log_local(f"Version: {VERSION}", "INFO")
    ecrire_log_local(f"Date: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}", "INFO")
    ecrire_log_local("=" * 80, "INFO")

    print(f"\n🔍 Directory configuration:")
    print(f"   📋 Logs    : {LOGS_DIR}")
    print(f"   📊 Results : {RESULTS_DIR}\n")

    ecrire_log_local(f"Logs directory: {LOGS_DIR}", "INFO")
    ecrire_log_local(f"Results directory: {RESULTS_DIR}", "INFO")

    # Dependencies check
    api_key = None
    if not args.simulate:
        manquantes = verifier_dependances()
        if manquantes:
            print("❌ Missing dependencies.")
            print(f"   Activate venv: source {ENV_DIR}/bin/activate")
            sys.exit(1)
        api_key = obtenir_api_key()

    # Load prompt
    from prompt_executor import PromptLoader
    loader = PromptLoader()

    if args.prompt_text:
        prompt_template = args.prompt_text
        print(f"🔍 Using direct prompt\n")
        ecrire_log_local("Prompt: Direct (command line)", "INFO")
    else:
        prompt_template = loader.load_prompt(args.prompt_file)
        if not prompt_template:
            print(f"❌ Prompt '{args.prompt_file}' not found")
            print("💡 Use --prompt-list to see available prompts")
            return
        print(f"🔍 Prompt loaded: {args.prompt_file}\n")
        ecrire_log_local(f"Prompt: {args.prompt_file}", "INFO")

    # Determine format
    if args.aiall:
        format_source = "auto"
    elif args.claude:
        format_source = "claude"
    elif args.chatgpt:
        format_source = "chatgpt"
    elif args.lechat:
        format_source = "lechat"
    else:
        format_source = "auto"

    ecrire_log_local(f"Source format: {format_source}", "INFO")

    # File search
    fichier_patterns = args.fichier if isinstance(args.fichier, list) else [args.fichier]
    fichiers_a_traiter = []

    for pattern in fichier_patterns:
        if args.recursive and '**' not in pattern:
            if os.path.isdir(pattern):
                pattern = os.path.join(pattern, '**', '*.json')
            elif '*' in pattern:
                base_dir = os.path.dirname(pattern) or '.'
                filename = os.path.basename(pattern)
                pattern = os.path.join(base_dir, '**', filename)
            else:
                base_dir = os.path.dirname(pattern) or '.'
                filename = os.path.basename(pattern)
                if filename:
                    pattern = os.path.join(base_dir, '**', filename)
                else:
                    pattern = os.path.join(pattern, '**', '*.json')

        if '**' in pattern or args.recursive:
            fichiers_trouves = glob.glob(pattern, recursive=True)
        else:
            fichiers_trouves = glob.glob(pattern)

        if fichiers_trouves:
            fichiers_a_traiter.extend(fichiers_trouves)

    if not fichiers_a_traiter:
        print(f"❌ No files found")
        ecrire_log_local("No files found", "ERROR")
        return

    fichiers_a_traiter = sorted(list(set(fichiers_a_traiter)))

    ecrire_log_local(f"Files to process: {len(fichiers_a_traiter)}", "INFO")
    for f in fichiers_a_traiter:
        ecrire_log_local(f"  - {f}", "INFO")

    print("╔" + "═" * 78 + "╗")
    print("║  AI Conversation Prompt Executor v3.0.2                          ║")
    print("╚" + "═" * 78 + "╝")
    print(f"📁 Files: {len(fichiers_a_traiter)}")
    print(f"🤖 Model: {args.model}")
    print(f"⚡ Workers: {args.workers}")
    print(f"📄 Format: {format_source.upper()}")
    if args.simulate:
        print("🧪 Mode: SIMULATION")
    print()

    # Loading
    toutes_conversations, stats_chargement, details_fichiers = charger_fichiers(fichiers_a_traiter, format_source)

    # Generate detailed file report
    generer_rapport_fichiers(details_fichiers, LOGS_DIR)

    if not toutes_conversations:
        print("\n❌ No conversations found.")
        ecrire_log_local("No conversations found", "ERROR")
        return

    print(f"\n{'─' * 70}")
    print(f"📊 Total loaded: {len(toutes_conversations)} conversations")
    print(f"{'─' * 70}\n")

    ecrire_log_local(f"Total conversations loaded: {len(toutes_conversations)}", "INFO")

    # Duplicate detection
    print("🔍 Detecting duplicates...")
    ecrire_log_local("Detecting duplicates...", "INFO")
    rapport_doublons = detecter_doublons(toutes_conversations)

    if rapport_doublons['nb_doublons'] > 0:
        print(f"⚠️  {rapport_doublons['nb_doublons']} duplicate(s) detected and excluded")
        ecrire_log_local(f"Duplicates detected: {rapport_doublons['nb_doublons']}", "WARNING")

        # Log duplicate details
        for doublon in rapport_doublons['doublons']:
            ecrire_log_local(
                f"  Duplicate: '{doublon['doublon']['titre']}' ({doublon['doublon']['fichier']}) "
                f"= '{doublon['original']['titre']}' ({doublon['original']['fichier']})",
                "WARNING"
            )
    else:
        print("✅ No duplicates detected")
        ecrire_log_local("No duplicates detected", "INFO")

    toutes_conversations = rapport_doublons['conversations_uniques']
    print()

    # Message extraction and splitting
    print("🔍 Extracting messages...")
    ecrire_log_local("Extracting messages...", "INFO")
    conversations_a_traiter = []

    for conv in toutes_conversations:
        format_conv = conv.get('_format', 'unknown')
        messages = extraire_messages(conv, format_conv)

        if not messages:
            continue

        # Split if necessary
        conversations_decoupees = decouper_conversation(conv, messages)
        for conv_decoupee in conversations_decoupees:
            # Preserve metadata
            conv_decoupee['_source_file'] = conv.get('_source_file', 'unknown')
            conv_decoupee['_format'] = format_conv
            conversations_a_traiter.append(conv_decoupee)

    print(f"✅ {len(conversations_a_traiter)} conversations ready (after splitting)\n")
    ecrire_log_local(f"Conversations ready: {len(conversations_a_traiter)}", "INFO")

    # Filtering if requested
    if args.cnbr is not None:
        if 0 < args.cnbr <= len(conversations_a_traiter):
            conversations_a_traiter = [conversations_a_traiter[args.cnbr - 1]]
            print(f"🎯 Analyzing only conversation #{args.cnbr}\n")
            ecrire_log_local(f"Filtering: conversation #{args.cnbr} only", "INFO")
        else:
            print(f"❌ --cnbr {args.cnbr} out of bounds (1-{len(conversations_a_traiter)})")
            ecrire_log_local(f"Error --cnbr: {args.cnbr} out of bounds", "ERROR")
            return

    if args.only_split:
        conversations_a_traiter = [c for c in conversations_a_traiter if '/' in c.get('partie', '')]
        print(f"✂️  Filtering: {len(conversations_a_traiter)} split conversations\n")
        ecrire_log_local(f"Filtering only-split: {len(conversations_a_traiter)} conversations", "INFO")

    if args.not_split:
        conversations_a_traiter = [c for c in conversations_a_traiter if c.get('partie', '') == '1/1']
        print(f"✅ Filtering: {len(conversations_a_traiter)} non-split conversations\n")
        ecrire_log_local(f"Filtering not-split: {len(conversations_a_traiter)} conversations", "INFO")

    if not conversations_a_traiter:
        print("❌ No conversations to process after filtering.")
        ecrire_log_local("No conversations after filtering", "ERROR")
        return

    # Executor initialization
    from prompt_executor import PromptExecutor, process_conversation_with_prompt

    executor = None
    if not args.simulate:
        executor = PromptExecutor(
            api_key=api_key,
            model=args.model
        )
        ecrire_log_local(f"Executor initialized: {args.model}", "INFO")
    else:
        # Simulation mode: create dummy executor
        class SimulateExecutor:
            def __init__(self):
                self.model = args.model
        executor = SimulateExecutor()
        ecrire_log_local("Simulation mode activated", "INFO")

    # Parallel execution
    print(f"🚀 Starting analysis ({args.workers} workers)...\n")
    ecrire_log_local(f"Starting analysis: {args.workers} workers, delay {args.delay}s", "INFO")
    resultats = []

    try:
        from tqdm import tqdm
    except ImportError:
        print("⚠️  tqdm module not available, progress without visual bar")
        ecrire_log_local("tqdm not available", "WARNING")
        tqdm = None

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}

        for conv in conversations_a_traiter:
            messages = conv.get('messages', [])
            future = pool.submit(
                process_conversation_with_prompt,
                conv,
                messages,
                prompt_template,
                executor,
                args.simulate,
                args.delay
            )
            futures[future] = conv.get('titre', 'Untitled')

        # Progress bar
        if tqdm:
            with tqdm(total=len(futures), desc="Analysis", unit="conv") as pbar:
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        resultats.append(result)

                        # Log each result
                        titre = result.get('titre', 'Untitled')
                        success = result.get('success', False)
                        if success:
                            ecrire_log_local(f"✅ Processed: {titre}", "INFO")
                        else:
                            error = result.get('error', 'Unknown error')
                            ecrire_log_local(f"❌ Failed: {titre} - {error}", "ERROR")

                        pbar.update(1)
                    except Exception as e:
                        titre = futures[future]
                        ecrire_log_local(f"Processing error '{titre}': {e}", "ERROR")
                        print(f"\n⚠️  Error: {titre}")
                        pbar.update(1)
        else:
            # Without tqdm
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    resultats.append(result)

                    # Log each result
                    titre = result.get('titre', 'Untitled')
                    success = result.get('success', False)
                    if success:
                        ecrire_log_local(f"✅ Processed: {titre}", "INFO")
                    else:
                        error = result.get('error', 'Unknown error')
                        ecrire_log_local(f"❌ Failed: {titre} - {error}", "ERROR")

                    completed += 1
                    if completed % 10 == 0:
                        print(f"   Progress: {completed}/{len(futures)}")
                except Exception as e:
                    titre = futures[future]
                    ecrire_log_local(f"Processing error '{titre}': {e}", "ERROR")
                    print(f"⚠️  Error: {titre}")
                    completed += 1

    # Save results
    print(f"\n💾 Saving results...")
    ecrire_log_local("Saving results...", "INFO")

    from result_formatter import ResultFormatter
    formatter = ResultFormatter()

    # Generate output filename
    if args.output:
        output_base = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_name = args.prompt_file if args.prompt_file else "custom"
        output_base = f"results_{prompt_name}_{timestamp}"

    # Add extension according to format
    if not any(output_base.endswith(ext) for ext in ['.csv', '.json', '.txt', '.md', '.markdown']):
        if args.format == 'csv':
            output_file = f"{output_base}.csv"
        elif args.format == 'json':
            output_file = f"{output_base}.json"
        elif args.format == 'txt':
            output_file = f"{output_base}.txt"
        elif args.format == 'markdown':
            output_file = f"{output_base}.md"
    else:
        output_file = output_base

    # Save in RESULTS_DIR
    output_path = RESULTS_DIR / output_file

    ecrire_log_local(f"Output file: {output_path}", "INFO")
    ecrire_log_local(f"Format: {args.format}", "INFO")

    # Save according to format
    success = False
    if args.format == 'csv':
        success = formatter.save_csv(resultats, str(output_path))
    elif args.format == 'json':
        success = formatter.save_json(resultats, str(output_path))
    elif args.format == 'txt':
        success = formatter.save_txt(resultats, str(output_path))
    elif args.format == 'markdown':
        success = formatter.save_markdown(resultats, str(output_path))

    if success:
        print(f"✅ Results saved: {output_path}")
        print(f"   📊 Format: {args.format.upper()}")
        file_size = os.path.getsize(output_path)
        print(f"   📏 Size: {file_size:,} bytes")
        ecrire_log_local(f"Results saved: {output_path} ({file_size} bytes)", "INFO")
    else:
        print(f"❌ Error during save")
        ecrire_log_local("Results save error", "ERROR")

    # Final statistics
    temps_total = time.time() - temps_debut
    success_count = sum(1 for r in resultats if r.get('success', False))
    error_count = len(resultats) - success_count

    print(f"\n{'═' * 70}")
    print(f"📊 FINAL REPORT")
    print(f"{'═' * 70}")
    print(f"⏱️  Total time: {temps_total:.2f}s")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {len(resultats)}")
    if len(resultats) > 0:
        print(f"📈 Success rate: {(success_count/len(resultats)*100):.1f}%")
    print(f"{'═' * 70}\n")

    ecrire_log_local("=" * 80, "INFO")
    ecrire_log_local("FINAL REPORT", "INFO")
    ecrire_log_local(f"Total time: {temps_total:.2f}s", "INFO")
    ecrire_log_local(f"Success: {success_count}", "INFO")
    ecrire_log_local(f"Errors: {error_count}", "INFO")
    ecrire_log_local(f"Total processed: {len(resultats)}", "INFO")
    if len(resultats) > 0:
        ecrire_log_local(f"Success rate: {(success_count/len(resultats)*100):.1f}%", "INFO")
    ecrire_log_local("=" * 80, "INFO")
    ecrire_log_local("ANALYSIS END", "INFO")


if __name__ == "__main__":
    # Automatic relaunch in venv if necessary
    venv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ENV_DIR)
    is_in_venv = hasattr(sys, 'real_prefix') or (sys.prefix != sys.base_prefix) or (venv_path in sys.executable)

    should_relaunch = (
        os.path.exists(venv_path) and
        not is_in_venv and
        '--install' not in sys.argv and
        '--help' not in sys.argv and
        '--help-adv' not in sys.argv and
        len(sys.argv) > 1
    )

    if should_relaunch:
        python_path = os.path.join(venv_path, "bin", "python3")
        if os.path.exists(python_path):
            try:
                os.execv(python_path, [python_path] + sys.argv)
            except Exception as e:
                print(f"⚠️  Warning: Failed to relaunch venv: {e}")

    main()
