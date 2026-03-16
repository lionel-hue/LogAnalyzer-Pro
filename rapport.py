import json
import os
import platform
from datetime import datetime

def generer_rapport(stats, fichiers_traites, source_dir):
    """
    Génère un fichier JSON horodaté dans le dossier 'rapports'.
    
    :param stats: dict contenant les statistiques calculées par le Module 1
    :param fichiers_traites: list des fichiers .log analysés
    :param source_dir: chemin du dossier source des logs
    """
    try:
    
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dossier_rapports = os.path.join(base_dir, "rapports")

        if not os.path.exists(dossier_rapports):
            os.makedirs(dossier_rapports)

       
        maintenant = datetime.now()
        date_fichier = maintenant.strftime("%Y-%m-%d")
        date_complet = maintenant.strftime("%Y-%m-%d %H:%M:%S")
        
        nom_fichier = f"rapport_{date_fichier}.json"
        chemin_final = os.path.join(dossier_rapports, nom_fichier)

        rapport = {
            "metadata": {
                "date": date_complet, 
                "utilisateur": os.environ.get('USER') or os.environ.get('USERNAME', 'Inconnu'), # [cite: 32, 29]
                "os": platform.system(), 
                "source": os.path.abspath(source_dir),  
                "version_outil": "LogAnalyzer Pro 1.0" 
            },
            "statistiques": {
                "total_lignes": stats.get("total_lignes", 0), 
                "par_niveau": { 
                    "INFO": stats.get("par_niveau", {}).get("INFO", 0),
                    "WARN": stats.get("par_niveau", {}).get("WARN", 0),
                    "ERROR": stats.get("par_niveau", {}).get("ERROR", 0)
                },
                "top5_erreurs": stats.get("top5_erreurs", []) 
            },
            "fichiers_traites": [os.path.abspath(f) for f in fichiers_traites] 
        }

    
        with open(chemin_final, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=4, ensure_ascii=False)

        print(f"[SUCCESS] Module Rapport : {nom_fichier} généré.")
        return chemin_final

    except Exception as e:
        print(f"[ERREUR] Échec du Module 2 : {e}")
        return None