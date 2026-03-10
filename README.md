# LogAnalyzer Pro

## 1. Description du projet et objectif
Outil CLI d'analyse, d'archivage et de supervision de logs applicatifs pour environnement DevOps.

## 2. Prérequis et installation
- Python 3.x installé.
- Aucune dépendance externe (Bibliothèque standard uniquement).
- Cloner le dépôt : `git clone [url]`

## 3. Utilisation
Exemple de commande :
```bash
python3 main.py --source ./logs_test --niveau ERROR --dest ./backups --retention 30
```

## 4. Description des modules
- `main.py` : Orchestration.
- `analyser.py` : Parsing et stats.
- `rapport.py` : Génération JSON.
- `archiver.py` : Compression et nettoyage.

## 5. Planification via Cron
Pour exécuter automatiquement l'outil tous les dimanches à 03h00, ajoutez la ligne suivante à votre crontab (`crontab -e`) :

0 3 * * 0 /usr/bin/python3 /chemin/absolu/vers/loganalyzer/main.py --source /chemin/absolu/vers/logs_test --dest /chemin/absolu/vers/backups

## 6. Répartition des tâches