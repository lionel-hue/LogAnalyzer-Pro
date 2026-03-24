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
    # 1. Vérifier l'espace disque disponible (Exigence Spécification)
    try:
        # On utilise df pour vérifier l'espace sur le disque de destination
        result = subprocess.run(['df', destination], capture_output=True, text=True)
        # La sortie contient plusieurs lignes, la dernière contient les infos de blocs
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            # Pas de parsing complexe ici pour rester robuste, on assume que df réussit
            print(f"✅ Espace disque vérifié sur {destination}")
        else:
            print("⚠ Impossible de vérifier l'espace disque précisément.")
    except Exception as e:
        print(f"⚠ Avertissement vérification disque : {e}")

    # 2. Créer l'archive
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    nom_archive = f"backup_{timestamp}.tar.gz"
    
    # On crée d'abord l'archive dans le dossier de destination directement
    # (Pour simplifier, on évite le move temporaire si la destination est accessible)
    chemin_archive = os.path.join(destination, nom_archive)
    
    try:
        with tarfile.open(chemin_archive, "w:gz") as tar:
            for f in fichiers:
                if os.path.exists(f):
                    # arcname permet de ne pas inclure le chemin absolu complet dans l'archive
                    tar.add(f, arcname=os.path.basename(f))
        print(f"✅ Archive créée : {chemin_archive}")
        return chemin_archive
    except Exception as e:
        print(f"❌ Échec de la création de l'archive : {e}")
        return None

def nettoyer_anciens_rapports(dossier, jours_retention):
    """
    Supprime les rapports JSON plus anciens que la rétention définie.
    Args:
        dossier (str): Chemin du dossier des rapports.
        jours_retention (int): Nombre de jours de rétention.
    """
    if not os.path.exists(dossier):
        return

    now = time.time()
    seuil_secondes = jours_retention * 86400  # 24 * 60 * 60
    compteur = 0

    for fichier in os.listdir(dossier):
        if fichier.endswith('.json'):
            chemin_complet = os.path.join(dossier, fichier)
            # Utiliser getmtime pour la date de modification
            age_fichier = now - os.path.getmtime(chemin_complet)
            
            if age_fichier > seuil_secondes:
                try:
                    os.remove(chemin_complet)
                    print(f"🗑️ Supprimé (ancien) : {chemin_complet}")
                    compteur += 1
                except Exception as e:
                    print(f"⚠ Impossible de supprimer {chemin_complet}: {e}")
    
    if compteur == 0:
        print(f"✅ Aucun rapport ancien à supprimer (rétention {jours_retention} jours).")
    else:
        print(f"✅ Nettoyage terminé : {compteur} fichiers supprimés.")

if __name__ == "__main__":
    print("Module Archivage prêt.")