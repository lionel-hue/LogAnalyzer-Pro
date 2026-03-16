#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 1 : Ingestion et Analyse des logs.
Responsable : Analyse des fichiers .log, filtrage et statistiques.
"""
import os
import glob
import platform
from collections import Counter
from datetime import datetime

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def analyser_logs(source, niveau):
    """
    Scanne le dossier source et analyse les logs selon le niveau.
    
    Args:
        source (str): Chemin absolu du dossier source.
        niveau (str): Niveau de filtrage (ERROR, WARN, INFO, ALL).
    
    Returns:
        dict: Dictionnaire contenant les statistiques et métadonnées.
    """
    # Normalisation du chemin source
    source_abs = os.path.abspath(source)
    
    # Recherche des fichiers .log
    motif = os.path.join(source_abs, "*.log")
    fichiers_logs = glob.glob(motif)
    
    statistiques = {"total": 0, "ERROR": 0, "WARN": 0, "INFO": 0}
    fichiers_traites = []
    
    for fichier in fichiers_logs:
        fichiers_traites.append(os.path.abspath(fichier))
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    
                    statistiques["total"] += 1
                    
                    # Parsing simple : on cherche le niveau dans la ligne
                    # Format supposé : YYYY-MM-DD HH:MM:SS NIVEAU Message
                    parties = ligne.split()
                    if len(parties) >= 4:
                        niveau_log = parties[2]
                        if niveau_log in statistiques:
                            statistiques[niveau_log] += 1
        except Exception as e:
            print(f"Avertissement : Impossible de lire {fichier} ({e})")

    # Filtrage si nécessaire (pour l'affichage ou retour spécifique)
    # Ici on retourne tout, le filtre peut être appliqué pour l'affichage
    
    resultat = {
        "metadata": {
            "os": platform.system(),
            "user": os.getenv("USER", "inconnu"),
            "date_analyse": datetime.now().isoformat(),
            "source": source_abs
        },
        "statistiques": statistiques,
        "fichiers_traites": fichiers_traites
    }
    
    return resultat

if __name__ == "__main__":
    print("Module Analyse prêt.")
    # Test rapide
    # print(analyser_logs("./logs_test", "ALL"))