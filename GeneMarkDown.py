from datetime import date
import GeneTexteEbook

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

# Génération de l'image en markdown

with open("Ebook_Markdown/cover.png", "wb") as f:
    f.write(GeneTexteEbook.image_bytes)