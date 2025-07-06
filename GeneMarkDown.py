from datetime import date
import os
import base64
import json

import GeneTexteEbook
import GeneCoverEbook

def generer_meta():
    """Génère le fichier meta.yaml"""
    # Créer le dossier s'il n'existe pas
    os.makedirs("Ebook_Markdown", exist_ok=True)
    
    # ✅ CORRIGER : Le titre est déjà avec guillemets dans meta.yaml, c'est bon
    # Mais assure-toi qu'il n'y a pas de guillemets dans le titre lui-même
    titre_clean = GeneTexteEbook.Titre.replace('"', '')
    print(titre_clean)
    
    meta_content = f"""title: "{titre_clean}"
author: "Alix Caperan"
date: "{date.today()}"
language: "fr"
"""
    
    with open("Ebook_Markdown/meta.yaml", "w", encoding="utf-8") as f:
        f.write(meta_content)
    print("✅ Fichier meta.yaml généré avec succès.")

def generer_markdown_complet():
    """Génère un fichier Markdown complet avec tous les chapitres."""
    
    # ✅ Charger les titres des chapitres depuis chapitres.json
    try:
        with open("Sauvegarde/chapitres.json", "r", encoding="utf-8") as f:
            chapitres_info = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier chapitres.json non trouvé.")
        return
    
    # ✅ Charger le contenu depuis full_chapitre.json
    try:
        with open("Sauvegarde/full_chapitre.json", "r", encoding="utf-8") as f:
            chapitres_contenu = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier full_chapitre.json non trouvé. Assurez-vous d'avoir exécuté GeneTexteEbook.py")
        return
    
    # Charger le titre du livre
    try:
        with open("Sauvegarde/titre.txt", "r", encoding="utf-8") as f:
            titre = f.read().strip().replace('"', '')
    except FileNotFoundError:
        titre = "Mon Roman"
    
    # ✅ CORRIGER : Enlever les guillemets du titre principal
    markdown_content = f"""# {titre}

*Par Alix Caperan*

---

"""
    
    # ✅ Combiner les infos des chapitres avec leur contenu
    for i in range(len(chapitres_contenu)):
        numero_chapitre = str(i + 1)
        
        # Récupérer le titre depuis chapitres.json
        if numero_chapitre in chapitres_info:
            titre_chapitre = chapitres_info[numero_chapitre]["titre"]
        else:
            titre_chapitre = f"Chapitre {numero_chapitre}"
        
        # Récupérer le contenu depuis full_chapitre.json
        contenu_chapitre = chapitres_contenu[i]
        
        # ✅ Nettoyer le contenu (enlever les titres redondants s'il y en a)
        import re
        lignes = contenu_chapitre.split('\n')
        contenu_nettoye = []
        
        for ligne in lignes:
            # Ignorer les lignes qui sont des titres de chapitre au début
            if not re.match(r'^#+\s*(Chapitre\s*\d+\s*:?.*)', ligne.strip()):
                contenu_nettoye.append(ligne)
            elif len(contenu_nettoye) > 0:  # Garder les titres qui ne sont pas au début
                contenu_nettoye.append(ligne)
        
        contenu_final = '\n'.join(contenu_nettoye).strip()
        
        # ✅ Ajouter le chapitre avec le bon format
        markdown_content += f"""## Chapitre {numero_chapitre} : {titre_chapitre}

{contenu_final}

---

"""
    
    # Sauvegarder le fichier complet
    with open("Ebook_Markdown/livre_complet.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"✅ Fichier livre_complet.md généré avec {len(chapitres_contenu)} chapitres")
    return "Ebook_Markdown/livre_complet.md"

def generer_cover():
    """Génère la couverture"""
    if GeneCoverEbook.image_base64:
        with open("Ebook_Markdown/cover.png", "wb") as f:
            f.write(base64.b64decode(GeneCoverEbook.image_base64))
        print("✅ Cover générée")

# ✅ PROTÉGER l'exécution automatique
if __name__ == "__main__":
    # Ce code ne s'exécute QUE si le fichier est lancé directement
    generer_meta()
    fichier_markdown = generer_markdown_complet()
    generer_cover()
    
    print("✅ Tous les fichiers Markdown générés")