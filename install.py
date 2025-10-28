#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Installation and verification module
Handles dependency installation and prerequisites verification
"""

import os
import sys
import shutil
import subprocess
import venv
from typing import List, Dict

# Ensure local imports are available or handle them
try:
    from config import ENV_DIR, DEPENDANCES
    from utils import ecrire_log
except ImportError:
    # Minimal fallback if initial import fails
    ENV_DIR = ".venv_analyse"
    DEPENDANCES = ["requests", "tqdm", "tiktoken", "mistletoe", "anthropic", "python-dotenv"]
    def ecrire_log(*args, **kwargs):
        pass


# Mapping of pip package names to their import names
PACKAGE_IMPORT_MAP: Dict[str, str] = {
    'tiktoken': 'tiktoken',
    'mistletoe': 'mistletoe',
    'anthropic': 'anthropic',
    'python-dotenv': 'dotenv',
    'tqdm': 'tqdm',
    'requests': 'requests',
}


def get_import_name(package_name: str) -> str:
    """Returns the import name corresponding to the pip package name."""
    return PACKAGE_IMPORT_MAP.get(package_name, package_name)


def verifier_prerequis_systeme() -> bool:
    """Verifies system prerequisites (Python3, permissions)."""
    ecrire_log("System prerequisites verification", "INFO")
    print("🔍 Checking system prerequisites...")
    pre_ok = True
    if not shutil.which("python3"):
        print("❌ Python3 not found")
        pre_ok = False
    print("✅ System prerequisites OK" if pre_ok else "❌ System prerequisites missing")
    return pre_ok


def verifier_dependances() -> List[str]:
    """
    Verifies dependencies. Returns a list of missing dependencies.
    If the venv doesn't exist, all dependencies are considered missing.
    """
    venv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ENV_DIR)

    if not os.path.exists(venv_path):
        return list(DEPENDANCES)

    manquantes = []
    python_path = os.path.join(venv_path, "bin", "python3")

    if not os.path.exists(python_path):
        return list(DEPENDANCES)

    # Use pip list to check installed packages (more reliable)
    pip_path = os.path.join(venv_path, "bin", "pip")

    try:
        result = subprocess.run(
            [pip_path, "list", "--format=freeze"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            installed_packages = set()
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    package_name = line.split('==')[0].lower()
                    installed_packages.add(package_name)

            # Check each dependency
            for dep in DEPENDANCES:
                package_name = dep.lower()
                if package_name not in installed_packages:
                    manquantes.append(dep)
        else:
            # Fallback to import check if pip list fails
            for dep in DEPENDANCES:
                import_name = get_import_name(dep)
                try:
                    result = subprocess.run(
                        [python_path, "-c", f"import {import_name}"],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode != 0:
                        manquantes.append(dep)
                except Exception:
                    manquantes.append(dep)
    except Exception as e:
        print(f"⚠️  Warning during dependency check: {e}")
        # Fallback to import check
        for dep in DEPENDANCES:
            import_name = get_import_name(dep)
            try:
                result = subprocess.run(
                    [python_path, "-c", f"import {import_name}"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode != 0:
                    manquantes.append(dep)
            except Exception:
                manquantes.append(dep)

    return manquantes


def verifier_prerequis_complet() -> None:
    """Verifies all complete prerequisites and displays the result."""
    verifier_prerequis_systeme()
    manquantes = verifier_dependances()

    if manquantes:
        if len(manquantes) == len(DEPENDANCES):
            print(f"\n❌ The venv ({ENV_DIR}) is not ready.")
        else:
            print(f"\n❌ Missing dependencies: {', '.join(manquantes)}.")

        print(f"   Please run the installation with: `./analyse_conversations_merged.py --install`")
    else:
        print("\n✅ All dependencies are installed and the environment is ready.")


def installer_dependances() -> bool:
    """Installs dependencies with a robustness loop."""
    ecrire_log("Installing dependencies", "INFO")

    if not os.path.exists(ENV_DIR):
        print(f"📦 Creating virtual environment...")
        try:
            venv.create(ENV_DIR, with_pip=True, symlinks=True)
            print("✅ Environment created.")
        except Exception as e:
            print(f"❌ Venv creation error: {e}")
            return False

    pip_path = os.path.join(ENV_DIR, "bin", "pip")
    if not os.path.exists(pip_path):
        print("❌ pip not found in venv.")
        return False

    # Update pip
    try:
        print("⚙️  Updating pip...")
        result = subprocess.run(
            [pip_path, "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ pip update failed: {e.stderr.strip()}")
        return False
    except subprocess.TimeoutExpired:
        print(f"❌ pip update timeout")
        return False

    # Installation loop with better error handling
    max_tentatives = 3
    for tentative in range(1, max_tentatives + 1):
        manquantes = verifier_dependances()

        if not manquantes:
            print("✅ All dependencies are installed.")
            return True

        if tentative > 1:
            print(f"🔄 Attempt {tentative}/{max_tentatives}: Re-installing missing packages...")
        else:
            print(f"📥 Installing {len(manquantes)} package(s): {', '.join(manquantes)}")

        try:
            # Install packages one by one for better error tracking
            failed_packages = []
            for package in manquantes:
                print(f"   Installing {package}...", end=' ')
                try:
                    result = subprocess.run(
                        [pip_path, "install", package],
                        capture_output=True,
                        text=True,
                        timeout=120,
                        check=True
                    )
                    print("✓")
                except subprocess.CalledProcessError as e:
                    print(f"✗")
                    print(f"      Error: {e.stderr.strip()[:200]}")
                    failed_packages.append(package)
                except subprocess.TimeoutExpired:
                    print(f"✗ (timeout)")
                    failed_packages.append(package)

            # Verification after this attempt
            encore_manquantes = verifier_dependances()

            if not encore_manquantes:
                print("✅ Installation completed successfully.")
                return True

            if failed_packages:
                print(f"⚠️  Failed packages: {', '.join(failed_packages)}")
                if tentative == max_tentatives:
                    print(f"\n💡 Try manual installation:")
                    print(f"   source {ENV_DIR}/bin/activate")
                    print(f"   pip install {' '.join(failed_packages)}")
                    return False

            if tentative < max_tentatives:
                continue

            # Last attempt failed
            print(f"❌ After {max_tentatives} attempts, packages are still missing: {', '.join(encore_manquantes)}")
            print(f"\n💡 Try manual installation:")
            print(f"   source {ENV_DIR}/bin/activate")
            print(f"   pip install {' '.join(encore_manquantes)}")
            return False

        except Exception as e:
            print(f"❌ Unexpected error during installation: {e}")
            if tentative == max_tentatives:
                return False

    return False


def supprimer_fichier(fichier: str, backup: bool = True) -> bool:
    """Deletes file with timestamped backup if requested."""
    from datetime import datetime

    if not os.path.exists(fichier):
        print(f"⚠️  File {fichier} not found")
        return False
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{fichier}.backup.{timestamp}"
        shutil.copy2(fichier, backup_file)
        print(f"💾 Backup: {backup_file}")
    os.remove(fichier)
    print(f"🗑️  Deleted: {fichier}")
    ecrire_log(f"Deleted {fichier} (backup: {backup_file if backup else 'no'})", "INFO")
    return True
