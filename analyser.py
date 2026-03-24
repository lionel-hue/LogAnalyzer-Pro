#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 1 : Ingestion et Analyse des logs.
Responsable : Membre 2 - Cœur de Logique
"""
import os
import glob
import platform
import getpass
from collections import Counter

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def analyser_logs(source, niveau):
    """
    Scanne le dossier source et analyse les logs selon le niveau.
    Retourne un dictionnaire structuré pour le rapport et l'orchestration.
    """
    # 1. Préparation du dictionnaire de stats (Le livrable propre)
    # On initialise la structure attendue par rapport.py et main.py
    stats = {
        "metadata": {
            "os": platform.system(),
            "user": getpass.getuser()
        },
        "statistiques": {
            "total": 0,
            "ERROR": 0,
            "WARN": 0,
            "INFO": 0,
            "top5_erreurs": []  # AJOUT : Champ requis par le spec
        },
        "fichiers_traites": []
    }
    
    toutes_les_erreurs = []
    comptage_niveaux = Counter()

    # 2. Utilisation de glob pour scanner les .log (Exigence Membre 2)
    motif = os.path.join(source, "*.log")
    fichiers_log = glob.glob(motif)

    for chemin_fichier in fichiers_log:
        # Conversion en chemin absolu pour le rapport
        chemin_absolu = os.path.abspath(chemin_fichier)
        stats["fichiers_traites"].append(chemin_absolu)
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    # 3. Parser les lignes (Format : YYYY-MM-DD HH:MM:SS NIVEAU Message)
                    parties = ligne.strip().split(' ', 3)
                    
                    if len(parties) >= 4:
                        log_niveau = parties[2]
                        message = parties[3]
                        
                        # 4. Filtrage par niveau (AJOUT)
                        # Si le niveau n'est pas ALL et ne correspond pas, on saute la ligne
                        if niveau != 'ALL' and log_niveau != niveau:
                            continue

                        # On compte tout pour les statistiques globales (sur les lignes filtrées)
                        stats["statistiques"]["total"] += 1
                        
                        if log_niveau in ["ERROR", "WARN", "INFO"]:
                            comptage_niveaux[log_niveau] += 1
                        
                        # On collecte toujours les erreurs pour le Top 5 (même si filtré par WARN, on garde trace si presente)
                        # Note: Si filtré par WARN, log_niveau != ERROR, donc cette ligne ne s'exécute pas.
                        # C'est cohérent avec "stats sur les logs analysés".
                        if log_niveau == "ERROR":
                            toutes_les_erreurs.append(message)
                            
        except Exception as e:
            print(f"Erreur de lecture sur {chemin_fichier}: {e}")

    # Mise à jour des compteurs spécifiques dans le dict statistiques
    stats["statistiques"]["ERROR"] = comptage_niveaux.get("ERROR", 0)
    stats["statistiques"]["WARN"] = comptage_niveaux.get("WARN", 0)
    stats["statistiques"]["INFO"] = comptage_niveaux.get("INFO", 0)
    
    # 5. Calcul du Top 5 des erreurs (AJOUT)
    top5 = Counter(toutes_les_erreurs).most_common(5)
    stats["statistiques"]["top5_erreurs"] = [msg for msg, count in top5]

    return stats

if __name__ == "__main__":
    dossier = "logs_test"
    print("\n" + "="*40)
    print(f" ANALYSE DU DOSSIER : {dossier}")
    print("="*40)
    resultat = analyser_logs(dossier, "ALL")
    if resultat["statistiques"]["total"] == 0:
        print("⚠ Attention : Aucune ligne lue. Vérifie tes fichiers .log !")
    else:
        print(f"✅ Total de lignes scannees : {resultat['statistiques']['total']}")
        print(f"📊 Statistiques par niveau : {resultat['statistiques']}")
        print(f"📁 Fichiers traités : {len(resultat['fichiers_traites'])}")
        print("-" * 40)
        print(f"💻 Système : {resultat['metadata']['os']}")
        print(f"👤 Utilisateur : {resultat['metadata']['user']}")
        print("="*40 + "\n")