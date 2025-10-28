#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilities module
Basic functions: logging, cleaning, token counting
"""

import os
import re
from datetime import datetime
from typing import Optional
from config import LOG_FILE, MAX_LOG_SIZE


def ecrire_log(message: str, niveau: str = "INFO") -> None:
    """Writes to log file with rotation."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{niveau}] {message}\n"
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) >= MAX_LOG_SIZE:
            backup_file = f"{LOG_FILE}.old"
            if os.path.exists(backup_file):
                os.remove(backup_file)
            os.rename(LOG_FILE, backup_file)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message)
    except Exception as e:
        print(f"⚠️  Log error: {e}")


def nettoyer_texte(texte: str) -> str:
    """Cleans text for analysis."""
    texte = re.sub(r'http\S+|www\S+', '', texte)
    texte = re.sub(r'\S+@\S+', '', texte)
    texte = re.sub(r'/[\w/.-]+|[A-Z]:\\[\w\\.-]+', '', texte)
    texte = re.sub(r'[^\w\s\u00C0-\u017F-]', ' ', texte)
    texte = ' '.join(texte.split())
    return texte.lower()


def compter_tokens(texte: str) -> int:
    """Counts tokens with fallback."""
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(texte))
    except Exception:
        return len(texte.split())


def generer_nom_sortie(
    fichier: str,
    multi_fichiers: bool = False,
    mode_local: bool = False,
    only_split: bool = False,
    not_split: bool = False
) -> str:
    """Generates the output CSV filename."""
    suffixes = []
    suffixes.append("local" if mode_local else "api")

    if only_split:
        suffixes.append("only_split")
    elif not_split:
        suffixes.append("not_split")

    suffix_str = "_".join(suffixes)

    if multi_fichiers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"topic_analysis_result_multi_{suffix_str}_{timestamp}.csv"
    else:
        nom_base = os.path.splitext(os.path.basename(fichier))[0]
        return f"topic_analysis_result_{nom_base}_{suffix_str}.csv"
