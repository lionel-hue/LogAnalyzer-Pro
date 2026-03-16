#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 4 : Point d'entrée et Orchestration.
Responsable : CLI argparse, gestion des erreurs, appel des modules.
"""
import argparse
import sys
import os

# Imports des modules collaborateurs
import analyser
import rapport
# import archiver  # TODO: Décommenter lorsque le module sera prêt

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """
    Fonction principale orchestrant le pipeline.
    """
    parser = argparse.ArgumentParser(description="LogAnalyzer Pro - Pipeline d'analyse")
    parser.add_argument("--source", required=True, help="Chemin vers le dossier logs")
    parser.add_argument("--niveau", default="ALL", choices=["ERROR", "WARN", "INFO", "ALL"])
    parser.add_argument("--dest", default="./backups", help="Dossier de destination des archives/rapports")
    parser.add_argument("--retention", type=int, default=30, help="Jours de rétention des rapports")
    
    args = parser.parse_args()
    
    # Validation du chemin source
    if not os.path.isdir(args.source):
        print(f"Erreur : Le dossier source '{args.source}' n'existe pas.", file=sys.stderr)
        sys.exit(1)

    try:
        print("Démarrage de LogAnalyzer Pro...")
        print(f"Source : {os.path.abspath(args.source)}")
        print(f"Niveau : {args.niveau}")
        
        # 1. Analyse (Module Collaborateur 2)
        print(">> Étape 1 : Analyse des logs...")
        stats = analyser.analyser_logs(args.source, args.niveau)
        total_logs = stats.get("statistiques", {}).get("total", 0)
        print(f"   Succès : {total_logs} lignes analysées dans {len(stats.get('fichiers_traites', []))} fichiers.")
        
        # 2. Rapport (Module Collaborateur 3)
        print(">> Étape 2 : Génération du rapport...")
        chemin_rapport = rapport.generer_rapport(stats, args.source, args.dest)
        print(f"   Succès : Rapport créé à {chemin_rapport}")
        
        # 3. Archivage (Module Collaborateur 4 - En attente)
        # print(">> Étape 3 : Archivage...")
        # archiver.archiver_logs([chemin_rapport], args.dest)
        print(">> Étape 3 : Archivage (En attente du module archiver.py)")
        
        print("\nPipeline terminé avec succès.")
        
    except Exception as e:
        print(f"Erreur fatale : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()