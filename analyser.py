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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def analyser_logs(source, niveau):
    """
    Scanne le dossier source et analyse les logs selon le niveau.
    """
    # 1. Préparation du dictionnaire de stats (Le livrable propre)
    stats = {
        "total_lignes": 0,
        "comptage_niveaux": Counter(),
        "top_5_erreurs": [],
        "metadata": {
            "os": platform.system(),
            "utilisateur": getpass.getuser()
        }
    }
    
    toutes_les_erreurs = []
    
    # 2. Utilisation de glob pour scanner les .log (Exigence Membre 2)
    motif = os.path.join(source, "*.log")
    fichiers_log = glob.glob(motif)

    for chemin_fichier in fichiers_log:
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    stats["total_lignes"] += 1
                    
                    # 3. Parser les lignes (Format : YYYY-MM-DD HH:MM:SS NIVEAU Message)
                    
                    parties = ligne.strip().split(' ', 3)
                    
                    if len(parties) >= 4:
                        log_niveau = parties[2]   
                        message = parties[3]      
                        
                        # 4. Calculer les stats et filtrer
                        if niveau == "ALL" or log_niveau == niveau:
                            stats["comptage_niveaux"][log_niveau] += 1
                            
                            
                            if log_niveau == "ERROR":
                                toutes_les_erreurs.append(message)
                                
        except Exception as e:
            print(f"Erreur de lecture sur {chemin_fichier}: {e}")

    # 5. Calculer le Top 5 erreurs et finaliser le dictionnaire
    stats["top_5_erreurs"] = Counter(toutes_les_erreurs).most_common(5)
    stats["comptage_niveaux"] = dict(stats["comptage_niveaux"])
    
    return stats


if __name__ == "__main__":
    dossier = "logs_test"
    
    print(f"\n" + "="*40)
    print(f"   ANALYSE DU DOSSIER : {dossier}")
    print("="*40)
    
    
    resultat = analyser_logs(dossier, "ALL")
    
    if resultat["total_lignes"] == 0:
        print("⚠ Attention : Aucune ligne lue. Vérifie tes fichiers .log !")
    else:
        print(f"✅ Total de lignes scannees : {resultat['total_lignes']}")
        print(f"📊 Statistiques par niveau : {resultat['comptage_niveaux']}")
        print(f"🔥 Top 5 des erreurs rencontrées :")
        for err, nb in resultat["top_5_erreurs"]:
            print(f"   - {err} ({nb} fois)")
        
        print("-" * 40)
        print(f"💻 Système : {resultat['metadata']['os']}")
        print(f"👤 Utilisateur : {resultat['metadata']['utilisateur']}")
    
    print("="*40 + "\n")