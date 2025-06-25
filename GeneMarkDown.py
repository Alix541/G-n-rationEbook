from datetime import date
import os
import base64

import GeneTexteEbook
import GeneCoverEbook

# Génération du fichier meta.yaml

meta_content = f"""title: "{GeneTexteEbook.Titre}"
author: "Axel Valladon"
date: "{date.today()}"
language: "fr"
"""

with open("Ebook_Markdown/meta.yaml", "w", encoding="utf-8") as f:
    f.write(meta_content)

print("✅ Fichier meta.yaml généré avec succès.")

# Génération des chapitres en markdown

for numero, contenu in GeneTexteEbook.ChapitresPourMarkdown.items():
    chemin_fichier = f"Ebook_Markdown/chapitre{numero}.md"
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write(f"# {contenu['titre']}\n\n")
        f.write(contenu['description'])
    print(f"✅ Fichier {chemin_fichier} généré")

# Affichage de la cover en png

cover_path = os.path.join("Ebook_Markdown", "cover.png")
cover_path = os.path.abspath(cover_path)

if  GeneCoverEbook.image_base64:
    with open("Ebook_Markdown/cover.png", "wb") as f:
        f.write(base64.b64decode(GeneCoverEbook.image_base64))