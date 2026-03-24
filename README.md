# LogAnalyzer Pro

## 1. Description du projet et objectif
Outil CLI d'analyse, d'archivage et de supervision de logs applicatifs pour environnement DevOps.
Ce projet valide la maîtrise des bibliothèques standard de Python appliquées à la programmation système.

## 2. Prérequis et installation
- Python 3.x installé.
- Aucune dépendance externe (Bibliothèque standard uniquement).
- Cloner le dépôt : `git clone [url]`

## 3. Utilisation
Exemple de commande :
```bash
python3 main.py --source ./logs_test --niveau ERROR --dest ./backups --retention 30
```

Arguments disponibles :
- `--source` : Chemin vers le dossier contenant les logs (obligatoire).
- `--niveau` : Filtrage (ERROR, WARN, INFO, ALL). Défaut : ALL.
- `--dest` : Dossier de sortie pour rapports et archives. Défaut : ./backups.
- `--retention` : Nombre de jours de conservation des rapports. Défaut : 30.

## 4. Description des modules
- `main.py` : Orchestration du pipeline, gestion des arguments et erreurs.
- `analyser.py` : Parsing des fichiers logs, calcul des statistiques et top erreurs.
- `rapport.py` : Génération du fichier JSON structuré et horodaté.
- `archiver.py` : Compression tar.gz, vérification disque et politique de rétention.

## 5. Planification via Cron
Pour exécuter automatiquement l'outil tous les dimanches à 03h00, ajoutez la ligne suivante à votre crontab (`crontab -e`) :

```bash
0 3 * * 0 /usr/bin/python3 /chemin/absolu/vers/loganalyzer/main.py --source /chemin/absolu/vers/logs_test --dest /chemin/absolu/vers/backups --retention 30
```

## 6. Répartition des tâches
| Membre | Rôle | Module | Responsabilités |
|--------|------|--------|----------------|
| Sisso Lionel Timileyin | Chef de Projet | `main.py` | Orchestration, argparse, gestion erreurs, README. |
| KOVOHOUANDE Espoir | Cœur de Logique | `analyser.py` | Parsing logs, glob, statistiques, top 5 erreurs. |
| TOSSOUGBO Mariel | Données & Rapport | `rapport.py` | Génération JSON, datetime, structure imposée. |
| LEGBANON Aurelle | Système & Archivage | `archiver.py` | Tarfile, shutil, rétention, espace disque. |
| TOUKOUROU Rodiath | Qualité & Tests | `logs_test/` | Données de test, validation intégration, Cron. |