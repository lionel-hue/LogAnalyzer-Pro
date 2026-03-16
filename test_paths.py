#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def check_for_relative_paths(filename):
    """Vérifie si le fichier utilise des chemins relatifs interdits."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        if '"./' in content or "'./" in content:
            print(f"❌ ERREUR dans {filename} : Chemin relatif détecté !")
        else:
            print(f"✅ {filename} semble respecter les chemins absolus.")

# Teste les fichiers de tes collègues
files_to_check = ['main.py', 'analyser.py', 'rapport.py', 'archiver.py']
for f in files_to_check:
    if os.path.exists(f):
        check_for_relative_paths(f)