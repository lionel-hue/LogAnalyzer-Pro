# 📋 Répartition des Tâches - LogAnalyzer Pro

**Équipe :** 5 Collaborateurs  
**Langue du projet :** Français  
**Deadline :** 25 mars 2026  
**Contrainte Majeure :** Bibliothèque standard Python uniquement & Chemins absolus (`__file__`).

---

## 👥 Répartition des Rôles

### 🟢 Membre 1 : Chef de Projet & Orchestration (`main.py`)
**Responsabilités :**
- Implémenter `main.py` (point d'entrée).
- Gérer `argparse` (arguments CLI : --source, --niveau, --dest, --retention).
- Orchestrer l'appel des fonctions des autres modules dans l'ordre.
- Gestion robuste des erreurs (`try/except`, `sys.exit(1)`).
- Fusionner les branches Git et gérer le `README.md` final.
- **Livrable :** `main.py` fonctionnel qui lance tout le pipeline.

### 🔵 Membre 2 : Cœur de Logique (`analyser.py`)
**Responsabilités :**
- Implémenter `analyser.py`.
- Utiliser `glob` pour scanner les `.log`.
- Parser les lignes (format : `YYYY-MM-DD HH:MM:SS NIVEAU Message`).
- Calculer les stats (Total, Comptage par niveau, Top 5 erreurs).
- Détecter OS et Utilisateur pour les métadonnées.
- **Livrable :** Fonction `analyser_logs` renvoyant un dict de stats propre.

### 🟣 Membre 3 : Données & Rapport (`rapport.py`)
**Responsabilités :**
- Implémenter `rapport.py`.
- Générer le fichier JSON `rapport_YYYY-MM-DD.json`.
- Respecter scrupuleusement la structure JSON imposée (metadata, statistiques, fichiers_traites).
- Utiliser `datetime` pour l'horodatage.
- S'assurer que les chemins dans le JSON sont absolus.
- **Livrable :** Fonction `generer_rapport` créant un JSON valide.

### 🟠 Membre 4 : Système & Archivage (`archiver.py`)
**Responsabilités :**
- Implémenter `archiver.py`.
- Créer l'archive `backup_YYYY-MM-DD.tar.gz` avec `tarfile`.
- Déplacer l'archive avec `shutil`.
- Implémenter la politique de rétention (suppression vieux JSON avec `os.path.getmtime`).
- Vérifier l'espace disque avec `subprocess` avant archivage.
- **Livrable :** Fonctions `archiver_logs` et `nettoyer_anciens_rapports`.

### 🔴 Membre 5 : Qualité, Tests & DevOps (`logs_test/` & Validation)
**Responsabilités :**
- Générer les données de test (`logs_test/app1.log`, `app2.log`, `app3.log`).
- Chaque fichier doit avoir ≥ 20 lignes (INFO, WARN, ERROR).
- Tester l'intégration complète (bout en bout).
- Valider la ligne Cron pour le README.
- Vérifier que **aucun chemin relatif** n'est utilisé dans le code.
- **Livrable :** Dossier `logs_test/` rempli + Rapport de test + Ligne Cron validée.

---

## 🛠 Contraintes Techniques Communes (À lire absolument)
1.  **Encodage :** Tous les fichiers doivent commencer par `# -*- coding: utf-8 -*-`.
2.  **Shebang :** Tous les fichiers `.py` doivent avoir `#!/usr/bin/env python3`.
3.  **Chemins :** Interdiction d'utiliser des chemins relatifs simples. Utiliser `os.path.abspath(__file__)` pour se baser.
4.  **Librairies :** **AUCUNE** librairie externe (pas de `pip install`). Uniquement `std lib`.
5.  **Documentation :** Chaque fonction doit avoir une `docstring` expliquée en français.

## 📅 Jalons (Suggestion)
- **Semaine 1 :** Completion des modules individuels (M2, M3, M4) + Données de test (M5).
- **Semaine 2 :** Intégration dans `main.py` (M1) + Tests d'intégration (M5).
- **Semaine 3 :** Correction bugs, Rédaction README, Démo finale.