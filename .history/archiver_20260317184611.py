#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 3 : Archivage et Nettoyage.
Responsable : Compression .tar.gz, déplacement et politique de rétention.
"""

import tarfile
import shutil
import os
import time
import subprocess

# Chemin absolu de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def archiver_logs(fichiers, destination):
    """
    Crée une archive tar.gz des fichiers logs.
    
    Args:
        fichiers (list): Liste des chemins absolus des fichiers à archiver.
        destination (str): Chemin du dossier de destination.
    
    Returns:
        str: Chemin de l'archive créée.
    """
    # TODO: Implémenter l'archivage
    pass

def nettoyer_anciens_rapports(dossier, jours_retention):
    """
    Supprime les rapports JSON plus anciens que la rétention définie.
    
    Args:
        dossier (str): Chemin du dossier des rapports.
        jours_retention (int): Nombre de jours de rétention.
    """
    # TODO: Implémenter le nettoyage
    pass

if __name__ == "__main__":
    print("Module Archivage prêt.")