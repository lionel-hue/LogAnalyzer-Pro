#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Archivage et Nettoyage.
Archive les fichiers .log traités en .tar.gz, déplace l'archive,
et supprime les anciens rapports JSON selon la politique de rétention.
"""

import os
import tarfile
import shutil
import time
import subprocess
from datetime import datetime


# Dossier rapports construit en chemin absolu depuis __file__
DOSSIER_RAPPORTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rapports")
DOSSIER_BACKUPS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")


def verifier_espace_disque(dossier_destination):
    """
    Vérifie l'espace disque disponible sur le dossier de destination via subprocess.
    Affiche un avertissement si l'espace est inférieur à 100 Mo.

    :param dossier_destination: Chemin du dossier de destination de l'archive
    """
    try:
        # Fonctionne sur Linux/macOS
        if os.name != "nt":
            result = subprocess.run(
                ["df", "-h", dossier_destination],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"[INFO] Espace disque disponible :\n{result.stdout}")
        else:
            # Windows : commande équivalente
            result = subprocess.run(
                ["wmic", "logicaldisk", "get", "size,freespace,caption"],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"[INFO] Espace disque disponible :\n{result.stdout}")
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"[WARN] Impossible de vérifier l'espace disque : {e}")


def creer_archive(fichiers_log, dossier_destination):
    """
    Crée une archive .tar.gz contenant tous les fichiers .log traités.
    L'archive est nommée backup_YYYY-MM-DD.tar.gz.

    :param fichiers_log: Liste des chemins absolus des fichiers .log à archiver
    :param dossier_destination: Dossier où déplacer l'archive finale
    :return: Chemin absolu de l'archive créée dans le dossier destination
    """
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)
        print(f"[INFO] Dossier créé : {dossier_destination}")

    date_today = datetime.now().strftime("%Y-%m-%d")
    nom_archive = f"backup_{date_today}.tar.gz"

    # Création de l'archive dans un dossier temporaire (répertoire courant du script)
    chemin_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), nom_archive)

    try:
        with tarfile.open(chemin_temp, "w:gz") as tar:
            for fichier in fichiers_log:
                if os.path.exists(fichier):
                    tar.add(fichier, arcname=os.path.basename(fichier))
                    print(f"[INFO] Ajouté à l'archive : {os.path.basename(fichier)}")
        print(f"[INFO] Archive créée : {chemin_temp}")
    except (tarfile.TarError, IOError, OSError) as e:
        raise RuntimeError(f"Erreur lors de la création de l'archive : {e}")

    # Déplacement de l'archive vers le dossier de destination
    chemin_final = os.path.join(dossier_destination, nom_archive)
    try:
        shutil.move(chemin_temp, chemin_final)
        print(f"[INFO] Archive déplacée vers : {chemin_final}")
    except (shutil.Error, OSError) as e:
        raise RuntimeError(f"Erreur lors du déplacement de l'archive : {e}")

    return chemin_final


def nettoyer_anciens_rapports(jours_retention):
    """
    Supprime les rapports JSON du dossier rapports/ dont l'âge dépasse
    le nombre de jours de rétention spécifié.

    :param jours_retention: Nombre de jours au-delà desquels un rapport est supprimé
    """
    if not os.path.exists(DOSSIER_RAPPORTS):
        print(f"[WARN] Dossier rapports introuvable : {DOSSIER_RAPPORTS}")
        return

    maintenant = time.time()
    limite_secondes = jours_retention * 86400  # 1 jour = 86400 secondes
    rapports_supprimes = 0

    for nom_fichier in os.listdir(DOSSIER_RAPPORTS):
        if not nom_fichier.endswith(".json"):
            continue

        chemin_fichier = os.path.join(DOSSIER_RAPPORTS, nom_fichier)
        age_fichier = maintenant - os.path.getmtime(chemin_fichier)

        if age_fichier > limite_secondes:
            try:
                os.remove(chemin_fichier)
                rapports_supprimes += 1
                print(f"[INFO] Rapport supprimé (> {jours_retention}j) : {nom_fichier}")
            except OSError as e:
                print(f"[WARN] Impossible de supprimer {nom_fichier} : {e}")

    if rapports_supprimes == 0:
        print(f"[INFO] Aucun rapport à supprimer (rétention : {jours_retention} jours)")
    else:
        print(f"[INFO] {rapports_supprimes} rapport(s) supprimé(s)")


def archiver_et_nettoyer(fichiers_log, dossier_destination, jours_retention):
    """
    Fonction principale du module : vérifie l'espace disque,
    crée l'archive .tar.gz, et nettoie les anciens rapports.

    :param fichiers_log: Liste des fichiers .log à archiver
    :param dossier_destination: Dossier de destination de l'archive
    :param jours_retention: Politique de rétention en jours
    :return: Chemin de l'archive créée
    """
    verifier_espace_disque(dossier_destination)
    chemin_archive = creer_archive(fichiers_log, dossier_destination)
    nettoyer_anciens_rapports(jours_retention)
    return chemin_archive
