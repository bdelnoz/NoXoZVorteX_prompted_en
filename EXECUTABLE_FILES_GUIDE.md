# 🚀 NoXoZVorteX_prompted - Executable Files Guide

## 📋 FICHIERS EXÉCUTABLES

Voici les fichiers Python que vous pouvez exécuter directement :

---

## 1. ✅ **analyse_conversations_merged.py** (PRINCIPAL)

**C'est le fichier PRINCIPAL à exécuter !**

### Usage:
```bash
./analyse_conversations_merged.py [OPTIONS]

# OU
python3 analyse_conversations_merged.py [OPTIONS]
```

### Fonctions:
- 🔧 Installation: `--install`
- ✅ Vérification: `--prerequis`
- ❓ Aide: `--help` ou `--help-adv`
- 📋 Liste prompts: `--prompt-list`
- 🚀 Exécution: `--exec`
- 📖 Changelog: `--changelog`

### Exemples:
```bash
# Installation
./analyse_conversations_merged.py --install

# Vérifier les prérequis
./analyse_conversations_merged.py --prerequis

# Lister les prompts disponibles
./analyse_conversations_merged.py --prompt-list

# Exécuter une analyse
./analyse_conversations_merged.py --exec \
  --aiall --fichier ./data/*.json \
  --prompt-file security_analysis \
  --format markdown
```

---

## 2. ✅ **test_features.py** (TESTS)

**Fichier pour tester que tout fonctionne correctement**

### Usage:
```bash
python3 test_features.py
```

### Fonction:
- Exécute une suite de tests complets
- Vérifie tous les modules
- Teste les fonctionnalités principales
- Génère un rapport de tests

### Quand l'exécuter:
- ✅ Après installation
- ✅ Après modifications du code
- ✅ Avant de commencer un projet important

### Résultat attendu:
```
╔════════════════════════════════════════════════════════════╗
║        ALL TESTS PASSED! ✅                                ║
╚════════════════════════════════════════════════════════════╝
```

---

## 3. ❌ **Fichiers NON EXÉCUTABLES** (Modules)

Ces fichiers sont des **modules** importés par le script principal.
**NE PAS les exécuter directement !**

### 📦 **config.py**
- Contient les configurations
- Variables globales
- Constantes du projet

### 📦 **extractors.py**
- Fonctions d'extraction de messages
- Détection de formats
- Parsing ChatGPT/Claude/LeChat

### 📦 **prompt_executor.py**
- Classes pour exécuter les prompts
- Gestion de l'API Mistral
- Formatage des prompts

### 📦 **result_formatter.py**
- Formatage des résultats
- Export CSV/JSON/TXT/Markdown

### 📦 **utils.py**
- Fonctions utilitaires
- Logging
- Comptage de tokens

### 📦 **install.py**
- Fonctions d'installation
- Vérification des dépendances

### 📦 **help.py**
- Système d'aide
- Affichage des messages d'aide

---

## 🎯 WORKFLOW RECOMMANDÉ

### 1️⃣ Première utilisation

```bash
# 1. Installation
./analyse_conversations_merged.py --install

# 2. Vérification
./analyse_conversations_merged.py --prerequis

# 3. Tests (optionnel)
python3 test_features.py

# 4. Configuration API
export MISTRAL_API_KEY='votre_clé'

# 5. Premier test
./analyse_conversations_merged.py --exec \
  --simulate \
  --prompt-file example_security_prompt \
  --fichier ./data_example/example_chatgpt_json.json
```

### 2️⃣ Utilisation quotidienne

```bash
# Simplement exécuter le script principal
./analyse_conversations_merged.py --exec \
  --aiall --fichier ./data/*.json \
  --prompt-file mon_prompt \
  --format markdown
```

---

## 📊 RÉSUMÉ VISUEL

```
NoXoZVorteX_prompted/
│
├── 🚀 analyse_conversations_merged.py  ← EXÉCUTER CELUI-CI !
├── ✅ test_features.py                 ← Tests (optionnel)
│
├── 📦 config.py                        ← Ne pas exécuter
├── 📦 extractors.py                    ← Ne pas exécuter
├── 📦 prompt_executor.py               ← Ne pas exécuter
├── 📦 result_formatter.py              ← Ne pas exécuter
├── 📦 utils.py                         ← Ne pas exécuter
├── 📦 install.py                       ← Ne pas exécuter
└── 📦 help.py                          ← Ne pas exécuter
```

---

## 🔑 COMMANDES ESSENTIELLES

### Installation et configuration
```bash
# 1. Installer
./analyse_conversations_merged.py --install

# 2. Vérifier
./analyse_conversations_merged.py --prerequis

# 3. Configurer API
export MISTRAL_API_KEY='votre_clé'
```

### Aide et information
```bash
# Aide basique
./analyse_conversations_merged.py --help

# Aide avancée
./analyse_conversations_merged.py --help-adv

# Liste des prompts
./analyse_conversations_merged.py --prompt-list

# Changelog
./analyse_conversations_merged.py --changelog
```

### Exécution
```bash
# Mode simulation (sans API)
./analyse_conversations_merged.py --exec --simulate \
  --prompt-file test --fichier sample.json

# Mode réel
./analyse_conversations_merged.py --exec \
  --aiall --fichier data/*.json \
  --prompt-file security_analysis \
  --format markdown
```

---

## ⚠️ ERREURS COURANTES

### Erreur: "Permission denied"
```bash
# Solution: Rendre le fichier exécutable
chmod +x analyse_conversations_merged.py
```

### Erreur: "No module named 'X'"
```bash
# Solution: Réinstaller
./analyse_conversations_merged.py --install
```

### Erreur: "MISTRAL_API_KEY not defined"
```bash
# Solution: Définir la clé
export MISTRAL_API_KEY='votre_clé'
```

---

## 💡 ASTUCES

### Créer un alias
```bash
# Dans votre ~/.bashrc ou ~/.zshrc
alias analyze='./analyse_conversations_merged.py --exec'

# Utilisation:
analyze --aiall --fichier data/*.json --prompt-file my_prompt
```

### Script wrapper
```bash
#!/bin/bash
# analyze.sh

export MISTRAL_API_KEY=$(cat ~/.mistral_key)

./analyse_conversations_merged.py --exec \
  --aiall --recursive \
  --fichier ./data/ \
  --prompt-file "$1" \
  --target-logs ./logs/$(date +%Y%m%d) \
  --target-results ./results/$(date +%Y%m%d) \
  --format markdown

# Utilisation:
# ./analyze.sh security_analysis
```

---

## 📞 BESOIN D'AIDE ?

```bash
# Afficher l'aide
./analyse_conversations_merged.py --help

# Aide avancée complète
./analyse_conversations_merged.py --help-adv

# Lire le README
cat README.md

# Lire le guide de démarrage
cat TRY_THIS_FIRST.txt
```

---

**Résumé**: 
- ✅ **EXÉCUTER**: `analyse_conversations_merged.py` (principal) et `test_features.py` (tests)
- ❌ **NE PAS EXÉCUTER**: Tous les autres fichiers .py (ce sont des modules)

**Commande la plus utilisée**:
```bash
./analyse_conversations_merged.py --exec --aiall --fichier data/*.json --prompt-file my_prompt
```
