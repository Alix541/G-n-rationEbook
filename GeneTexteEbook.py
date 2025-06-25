import getpass
import os
import inspect
from typing import Optional, List
from pydantic import BaseModel, Field
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import Tool, initialize_agent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent_types import AgentType
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate

from openai import OpenAI
import base64

import categorie
import ClassPers
import ClassMonde
import ClassTram

os.environ["LANGSMITH_TRACING"] = "true"
if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = "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"
if "LANDSMITH_PROJECT" not in os.environ:
    os.environ["LANGSMITH_PROJECT"]="default"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"]="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"


model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
struct_roman=categorie.tirer_scenario()

# struct_roman
struct_roman_path = "Sauvegarde/struct_roman.json"
if os.path.exists(struct_roman_path):
    with open(struct_roman_path, "r", encoding="utf-8") as f:
        struct_roman = json.load(f)
    print("📖 struct_roman chargé depuis la sauvegarde !")
else:
    struct_roman = categorie.tirer_scenario()
    with open(struct_roman_path, "w", encoding="utf-8") as f:
        json.dump(struct_roman, f, ensure_ascii=False, indent=2)
    print("📖 struct_roman généré et sauvegardé !")

# Génération du shema narratif principal

SCHEMA_PRINCIPAL_CLASSES = {
    name: cls
    for name, cls in inspect.getmembers(ClassTram, inspect.isclass)
    if cls.__module__ == ClassTram.__name__
}

shema_principal_path = "Sauvegarde/shema_narratif_principal.json"
if os.path.exists(shema_principal_path):
    with open(shema_principal_path, "r", encoding="utf-8") as f:
        Shema_narratif_principal = json.load(f)
    print("📝 Schéma narratif principal chargé depuis la sauvegarde !")
else:
    schema_principal_class = SCHEMA_PRINCIPAL_CLASSES[struct_roman["schema_principal"]]
    Shema_principale_struct = model.with_structured_output(schema_principal_class)
    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content=f"Ta mission est de générer les shema narratif principale de l'histoire sous la forme d'un {struct_roman['schema_principal']}."),
        SystemMessage(content=f"La structure du roman est la suivante: {struct_roman}"),
        HumanMessage(content=f"Ecrit le shema narratif principal, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
    ]
    Shema_narratif_principal = Shema_principale_struct.invoke(message).model_dump()
    with open(shema_principal_path, "w", encoding="utf-8") as f:
        json.dump(Shema_narratif_principal, f, ensure_ascii=False, indent=2)
    print("📝 Schéma narratif principal généré et sauvegardé !")

# Génération du monde ou se passe l'histoire

monde_path = "Sauvegarde/monde_sauvegarde.json"
if os.path.exists(monde_path):
    with open(monde_path, "r", encoding="utf-8") as f:
        Monde = json.load(f)
    print("🌍 Monde chargé depuis la sauvegarde !")
else:
    monde_struct = model.with_structured_output(ClassMonde.Monde)

    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content=f"Ta mission est de générer un monde fictif où l'histoire prend places"),
        SystemMessage(content=f"Tu dois prendre en compte la structure suivante : {struct_roman}"),
        SystemMessage(content=f"Tu dois prendre le shema narratif suivant : {Shema_narratif_principal}"),
        HumanMessage(content="Génère un monde fictif cohérent avec la structure du roman et le schéma narratif principal")
    ]

    Monde = monde_struct.invoke(message).model_dump()
    with open(monde_path, "w", encoding="utf-8") as f:
        json.dump(Monde, f, ensure_ascii=False, indent=2)
    print("🌍 Monde généré et sauvegardé !")

# Génération des personnages

personnages_path = "Sauvegarde/personnages.json"
if os.path.exists(personnages_path):
    with open(personnages_path, "r", encoding="utf-8") as f:
        PersonnageDict = json.load(f)
    print("👤 Personnages chargés depuis la sauvegarde !")
else:
    Pers_struct = model.with_structured_output(ClassPers.ListePersonnages)
    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content="Ta mission est de générer des personnages cohérents avec l'univers donné."),
        SystemMessage(content=f"Structure du roman : {struct_roman}"),
        SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
        SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
        HumanMessage(content="Génère un personnage principal, selon les besoins entre 3 à 5 personnages secondaires majeurs et entre 1 et 5 personnages secondaires mineurs")
    ]
    PersonnageDict = Pers_struct.invoke(message).model_dump()
    with open(personnages_path, "w", encoding="utf-8") as f:
        json.dump(PersonnageDict, f, ensure_ascii=False, indent=2)
    print("👤 Personnages générés et sauvegardés !")

# Génération du shema narratif complémentaire

shema_complementaire_path = "Sauvegarde/shema_complementaire_narratif.json"
if os.path.exists(shema_complementaire_path):
    with open(shema_complementaire_path, "r", encoding="utf-8") as f:
        Shema_complementaire_narratif = json.load(f)
    print("📝 Schéma narratif complémentaire chargé depuis la sauvegarde !")
else:
    SHEMA_COMPLEMENTAIRE_CLASSES = {
        name: clas
        for name, clas in inspect.getmembers(ClassTram, inspect.isclass)
        if clas.__module__ == ClassTram.__name__
    }
    Shema_complementaire_struct = model.with_structured_output(SHEMA_COMPLEMENTAIRE_CLASSES[struct_roman["schema_complementaire"]])
    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content=f"Ta mission est de générer les shema narratif secondaire de l'histoire sous la forme d'un {struct_roman['schema_complementaire']}."),
        SystemMessage(content=f"La structure du roman est la suivante : {struct_roman}"),
        SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
        SystemMessage(content=f"Shema narratif principal de l'histoire : {Shema_narratif_principal}"),
        HumanMessage(content=f"Ecrit un shema narratif secondaire, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
    ]
    Shema_complementaire_narratif = Shema_complementaire_struct.invoke(message).model_dump()
    with open(shema_complementaire_path, "w", encoding="utf-8") as f:
        json.dump(Shema_complementaire_narratif, f, ensure_ascii=False, indent=2)
    print("📝 Schéma narratif complémentaire généré et sauvegardé !")

# Génération des chapitres avec une description pour chaque chapitre

class ChapitreClass(BaseModel):
    titre: str = Field(description="Le titre du chapitre")
    description: str = Field(description="Une courte description de, 3 à 4 lignes de ce qui va se passer dans le chapitre")

class ListeChapitres(BaseModel):
    """Une liste de chapitres pour le roman"""
    chapitres: List[ChapitreClass] = Field(description="Liste des chapitres du roman avec titre et description")

chapitres_path = "Sauvegarde/chapitres.json"
if os.path.exists(chapitres_path):
    with open(chapitres_path, "r", encoding="utf-8") as f:
        ChapitresPourMarkdown = json.load(f)
    print("📚 Chapitres chargés depuis la sauvegarde !")
else:
    Chapitres_struct = model.with_structured_output(ListeChapitres)
    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content="Ta mission est de générer la liste des chapitres du roman. Pour chaque chapitre, donne un titre et une description de quelques lignes expliquant ce qui va se passer dans le chapitre."),
        SystemMessage(content=f"Nombre de chapitres: {struct_roman['nombre_chapitres']}"),
        SystemMessage(content=f"Structure du roman : {struct_roman}"),
        SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
        SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
        SystemMessage(content=f"Schéma narratif complémentaire de l'histoire : {Shema_complementaire_narratif}"),
        SystemMessage(content=f"Liste des personnages : {PersonnageDict}"),
        HumanMessage(content="Génère la liste complète des chapitres du roman avec une description de quelques lignes pour chaque chapitre.")
    ]
    Chapitres = Chapitres_struct.invoke(message).model_dump()
    ChapitresPourMarkdown = { i + 1: chapitre for i, chapitre in enumerate(Chapitres['chapitres']) }
    with open(chapitres_path, "w", encoding="utf-8") as f:
        json.dump(ChapitresPourMarkdown, f, ensure_ascii=False, indent=2)
    print("📚 Chapitres générés et sauvegardés !")

# Génération du titre du roman

titre_path = "Sauvegarde/titre.txt"
if os.path.exists(titre_path):
    with open(titre_path, "r", encoding="utf-8") as f:
        Titre = f.read().strip()
    print("🏷️ Titre chargé depuis la sauvegarde !")
else:
    message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content="Ta mission est de générer le titre du roman."),
        SystemMessage(content=f"Structure du roman : {struct_roman}"),
        SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
        SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
        SystemMessage(content=f"Schéma narratif complémentaire de l'histoire : {Shema_complementaire_narratif}"),
        SystemMessage(content=f"Liste des personnages : {PersonnageDict}"),
        SystemMessage(content=f"Liste des chapitres : {ChapitresPourMarkdown}"),
        SystemMessage(content=f"Retourne que le titre du roman, sans explication ni description, juste le titre."),
        HumanMessage(content="Propose un titre original et accrocheur pour ce roman.")
    ]
    Titre = model.invoke(message).content
    with open(titre_path, "w", encoding="utf-8") as f:
        f.write(Titre)
    print("🏷️ Titre généré et sauvegardé !")

# Génération du roman en entier

TabPreviousChap=[]
ChapitreEntier=[]
nbchap=0

message = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content=f"Ta mission est d'écrire un chapitre entier du roman, en respectant la taille indiquée qui est de environ {struct_roman['caracteres_par_chapitre']} caractères)."),
        SystemMessage(content="À la fin du chapitre, fournis un résumé détaillé de tout ce qui est utile pour écrire le chapitre suivant et pour assurer la cohérence de l'histoire. Ce résumé doit inclure les éléments importants, les évolutions des personnages, les enjeux, et tout ce qui doit être gardé en mémoire pour la suite."),
        SystemMessage(content="Le résumé doit être clairement séparé du texte du chapitre, par exemple avec une balise spéciale comme '---RESUME---' pour faciliter la séparation automatique."),
        SystemMessage(content=f"Voici la structure du roman : {struct_roman}"),
        SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
        SystemMessage(content=f"Schéma narratif principal (à garder en mémoire) : {Shema_narratif_principal}"),
        SystemMessage(content=f"Schéma narratif complémentaire (à garder en mémoire) : {Shema_complementaire_narratif}"),
        SystemMessage(content=f"Liste des personnages (à garder en mémoire): {PersonnageDict}"),
        SystemMessage(content=f"Résumé rapide de l'idée principale du chapitre à écrire : {ChapitresPourMarkdown[nbchap]['description']}"),
        SystemMessage(content="N'oublie pas de respecter la cohérence avec les chapitres précédents et d'assurer la continuité de l'intrigue."),
        HumanMessage(content="Écris le chapitre complet, puis ajoute le résumé séparé par '---RESUME---'.")
]
