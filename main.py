#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 4 : Point d'entrée et Orchestration.
Responsable : Membre 1 - Chef de Projet
"""
import argparse
import sys
import os

# Imports des modules collaborateurs
import analyser
import rapport
import archiver  # ✅ Décommenté pour intégration

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

    # Conversion des chemins en absolus dès l'entrée (Contrainte Info.md)
    source_abs = os.path.abspath(args.source)
    dest_abs = os.path.abspath(args.dest)

    # Validation du chemin source
    if not os.path.isdir(source_abs):
        print(f"Erreur : Le dossier source '{source_abs}' n'existe pas.", file=sys.stderr)
        sys.exit(1)

    try:
        print("Démarrage de LogAnalyzer Pro...")
        print(f"Source : {source_abs}")
        print(f"Niveau : {args.niveau}")
        print(f"Destination : {dest_abs}")
        print("-" * 40)

        # 1. Analyse (Module Collaborateur 2)
        print(">> Étape 1 : Analyse des logs...")
        stats = analyser.analyser_logs(source_abs, args.niveau)
        total_logs = stats.get("statistiques", {}).get("total", 0)
        nb_fichiers = len(stats.get("fichiers_traites", []))
        print(f"   Succès : {total_logs} lignes analysées dans {nb_fichiers} fichiers.")

        # 2. Rapport (Module Collaborateur 3)
        print(">> Étape 2 : Génération du rapport...")
        chemin_rapport = rapport.generer_rapport(stats, source_abs, dest_abs)
        print(f"   Succès : Rapport créé à {chemin_rapport}")

        # 3. Archivage (Module Collaborateur 4) ✅ Intégré
        print(">> Étape 3 : Archivage...")
        # On archive les fichiers LOGS traités (pas le rapport JSON lui-même selon spec Module 3)
        archiver.archiver_logs(stats["fichiers_traites"], dest_abs)
        
        # 4. Nettoyage (Module Collaborateur 4) ✅ Intégré
        print(">> Étape 4 : Nettoyage des anciens rapports...")
        archiver.nettoyer_anciens_rapports(dest_abs, args.retention)

        print("-" * 40)
        print("\nPipeline terminé avec succès.")

    except Exception as e:
        print(f"Erreur fatale : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()