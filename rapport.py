#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 2 : Génération du Rapport JSON.
Responsable : Création du fichier JSON structuré selon les spécifications.
"""

import json
import datetime
import os

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generer_rapport(statistiques, source, dossier_sortie):
    """
    Génère un fichier JSON horodaté avec les statistiques.
    
    Args:
        statistiques (dict): Données issues du module analyser.
        source (str): Chemin source analysé.
        dossier_sortie (str): Chemin où sauvegarder le rapport.
    
    Returns:
        str: Chemin absolu du fichier rapport créé.
    """
    # TODO: Implémenter la génération JSON
    pass

if __name__ == "__main__":
    print("Module Rapport prêt.")