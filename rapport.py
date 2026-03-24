#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 2 : Génération du Rapport JSON.
Responsable : Membre 3 - Données & Rapport
"""
import json
import datetime
import os

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generer_rapport(statistiques, source, dossier_sortie):
    """
    Génère un fichier JSON horodaté avec les statistiques.
    Respecte la structure imposée dans les backups.
    """
    # Assurance que le dossier de sortie existe (chemin absolu)
    dossier_abs = os.path.abspath(dossier_sortie)
    os.makedirs(dossier_abs, exist_ok=True)

    # Nom du fichier avec timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier = f"rapport_{timestamp}.json"
    chemin_complet = os.path.join(dossier_abs, nom_fichier)

    # Construction du rapport final pour matcher l'exemple backups/rapport_*.json
    # Note: statistiques.get("statistiques") contient maintenant top5_erreurs grâce à analyser.py
    rapport_final = {
        "metadata": {
            "os": statistiques.get("metadata", {}).get("os", "Unknown"),
            "user": statistiques.get("metadata", {}).get("user", "Unknown"),
            "date_analyse": datetime.datetime.now().isoformat(),
            "source": os.path.abspath(source)
        },
        "statistiques": statistiques.get("statistiques", {}),
        "fichiers_traites": statistiques.get("fichiers_traites", [])
    }

    try:
        with open(chemin_complet, 'w', encoding='utf-8') as f:
            json.dump(rapport_final, f, indent=4, ensure_ascii=False)
        return os.path.abspath(chemin_complet)
    except Exception as e:
        raise IOError(f"Échec de l'écriture du rapport : {e}")

if __name__ == "__main__":
    print("Module Rapport prêt.")