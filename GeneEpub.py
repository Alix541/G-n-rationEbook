import subprocess
import os

def generer_epub():
    """Génère automatiquement l'EPUB avec Pandoc."""
    
    # ✅ IMPORTER seulement quand nécessaire
    try:
        import GeneMarkDown
        import GeneTexteEbook
    except Exception as e:
        print(f"❌ Erreur lors de l'import : {e}")
        print("🔧 Assurez-vous que les fichiers de sauvegarde existent")
        return None
    
    # ✅ Générer automatiquement les fichiers Markdown d'abord
    print("📝 Génération des fichiers Markdown...")
    try:
        GeneMarkDown.generer_meta()
        GeneMarkDown.generer_markdown_complet()
        GeneMarkDown.generer_cover()
        print("✅ Fichiers Markdown générés")
    except Exception as e:
        print(f"❌ Erreur lors de la génération Markdown : {e}")
        return None
    
    # ✅ Créer le dossier Epub s'il n'existe pas
    os.makedirs("Epub", exist_ok=True)
    
    # Aller dans le dossier Ebook_Markdown pour accéder aux fichiers sources
    original_dir = os.getcwd()
    os.chdir("Ebook_Markdown")
    
    try:
        # Nom de l'EPUB (nettoyer le titre)
        titre_propre = GeneTexteEbook.Titre.replace(' ', '_').replace(':', '').replace('?', '').replace('!', '').replace('"', '')
        nom_epub = f"{titre_propre}.epub"
        
        # ✅ Chemin complet vers le dossier Epub (depuis Ebook_Markdown)
        epub_output_path = os.path.join("..", "Epub", nom_epub)
        
        # ✅ Commande Pandoc avec sortie vers le dossier Epub
        commande = [
            "pandoc",
            "meta.yaml",
            "livre_complet.md",
            "-o", epub_output_path,
            "--epub-cover-image=cover.png",
            "--split-level=2",
            "--toc",
            "--toc-depth=2"
        ]
        
        print("🔄 Génération de l'EPUB en cours...")
        print(f"📝 Commande : {' '.join(commande)}")
        
        result = subprocess.run(commande, check=True, capture_output=True, text=True)
        
        epub_path = os.path.abspath(epub_output_path)
        print(f"✅ EPUB généré avec succès : {epub_path}")
        return epub_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la génération : {e}")
        print(f"Sortie d'erreur : {e.stderr}")
        return None
    except FileNotFoundError:
        print("❌ Pandoc n'est pas installé.")
        print("Installez-le avec : winget install pandoc")
        return None
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    print("🚀 Démarrage de la génération complète EPUB...")
    print("📝 Étape 1/2 : Génération des fichiers Markdown")
    print("📚 Étape 2/2 : Conversion en EPUB")
    print("-" * 50)
    
    epub_path = generer_epub()
    if epub_path:
        print(f"\n📚 Votre EPUB est prêt !")