#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Module
Contains all project constants and configurations
"""

import os

# Metadata
VERSION = "v3.0.2"
DATE = "2025-10-19"
AUTHOR = "Bruno DELNOZ - bruno.delnoz@protonmail.com"

# Files and paths
LOG_FILE = "log.analyse_chatgpt.v2.7.0.log"
INPUT_FILE = "AI_exportation_bruno.delnoz_protonmail.com_conversations.json"
ENV_DIR = ".venv_analyse"

# Limits and configurations
MAX_LOG_SIZE = 2 * 1024 * 1024  # 2 MB
MAX_TOKENS = 31000
MAX_WORKERS = 5

# API Configuration
API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "pixtral-large-latest"

# Python Dependencies
DEPENDANCES = ["requests", "tqdm", "tiktoken", "mistletoe", "anthropic", "python-dotenv"]

# French and English stopwords
STOPWORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
    'dans', 'sur', 'pour', 'par', 'avec', 'sans', 'sous', 'est', 'sont',
    'a', 'ai', 'as', 'ont', 'été', 'être', 'avoir', 'fait', 'faire',
    'cette', 'ce', 'ces', 'cet', 'il', 'elle', 'on', 'nous', 'vous', 'ils',
    'elles', 'je', 'tu', 'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes',
    'ses', 'qui', 'que', 'quoi', 'dont', 'où', 'quand', 'comment', 'pourquoi',
    'si', 'comme', 'plus', 'moins', 'très', 'trop', 'peu', 'beaucoup',
    'tout', 'tous', 'toute', 'toutes', 'autre', 'autres', 'même', 'aussi',
    'ne', 'pas', 'non', 'oui', 'peut', 'peux', 'peuvent', 'va', 'vais', 'vas',
    'allons', 'allez', 'vont', 'ça', 'cela', 'celui', 'celle', 'ceux', 'celles',
    'donc', 'alors', 'ainsi', 'car', 'bien', 'encore', 'déjà', 'ici', 'là',
    'voici', 'voilà', 'au', 'aux', 'en', 'y', 'à', 'the', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'of',
    'to', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'by', 'with', 'from',
    'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'can', 'just', 'now', 'me',
    'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
    'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'an', 'as', 'because', 'until', 'while', 'get',
    'got', 'j', 'c', 'l', 'd', 'n', 's', 't', 'm', 'qu', 'y', 'va', 'veux',
    'voir', 'dire', 'dit', 'sais', 'sait', 'faut', 'pense', 'crois', 'vois'
}

def obtenir_api_key() -> str:
    """Retrieves the API key from environment."""
    api_key = os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        print("❌ MISTRAL_API_KEY environment variable not defined.")
        print("💡 Define it with: export MISTRAL_API_KEY='your_key'")
        import sys
        sys.exit(1)
    return api_key
