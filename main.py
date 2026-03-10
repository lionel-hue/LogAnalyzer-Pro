#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 4 : Point d'entrée et Orchestration.
Responsable : CLI argparse, gestion des erreurs, appel des modules.
"""

import argparse
import sys
import os

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """
    Fonction principale orchestrant le pipeline.
    """
    parser = argparse.ArgumentParser(description="LogAnalyzer Pro - Pipeline d'analyse")
    parser.add_argument("--source", required=True, help="Chemin vers le dossier logs")
    parser.add_argument("--niveau", default="ALL", choices=["ERROR", "WARN", "INFO", "ALL"])
    parser.add_argument("--dest", default="./backups", help="Dossier de destination des archives")
    parser.add_argument("--retention", type=int, default=30, help="Jours de rétention des rapports")
    
    args = parser.parse_args()
    
    try:
        # TODO: Orchestration des modules (analyser -> rapport -> archiver)
        print("Démarrage de LogAnalyzer Pro...")
        pass
    except Exception as e:
        print(f"Erreur fatale : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()