import getpass
import os
import inspect
from typing import Optional, List
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import Tool, initialize_agent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent_types import AgentType

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

# Génération du shema narratif principal

SCHEMA_PRINCIPAL_CLASSES = {
    name: cls
    for name, cls in inspect.getmembers(ClassTram, inspect.isclass)
    if cls.__module__ == ClassTram.__name__
}

schema_principal_class = SCHEMA_PRINCIPAL_CLASSES[struct_roman["schema_principal"]]
Shema_principale_struct = model.with_structured_output(schema_principal_class)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer les shema narratif principale de l'histoire sous la forme d'un {struct_roman['schema_principal']}."),
    SystemMessage(content=f"La structure du roman est la suivante: {struct_roman}"),
    HumanMessage(content=f"Ecrit le shema narratif principal, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
]

Shema_narratif_principal = Shema_principale_struct.invoke(message).model_dump()
print(Shema_narratif_principal, "\n\nSchéma narratif principal généré avec succès !")

# Génération du monde ou se passe l'histoire

monde_struct = model.with_structured_output(ClassMonde.Monde)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer un monde fictif où l'histoire prend places"),
    SystemMessage(content=f"Tu dois prendre en compte la structure suivante : {struct_roman}"),
    SystemMessage(content=f"Tu dois prendre le shema narratif suivant : {Shema_narratif_principal}"),
    HumanMessage(content="Génère un monde fictif cohérent avec la structure du roman et le schéma narratif principal")
]

Monde = monde_struct.invoke(message).model_dump()
print(Monde, "\n\nMonde généré avec succès !")

# Génération des personnages

Pers_struct = model.with_structured_output(ClassPers.ListePersonnages)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content="Ta mission est de générer des personnages cohérents avec l'univers donné."),
    SystemMessage(content=f"Structure du roman : {struct_roman}"),
    SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
    HumanMessage(content="Génère un personnage principal, selon les besoins entre 3 et 5 personnages secondaires majeurs et entre 1 et 5 personnages secondaires mineurs")
]

PersonnageDict = Pers_struct.invoke(message).model_dump()
print(PersonnageDict, "\n\nPersonnages générés avec succès !")

# Génération du shema narratif complémentaire

SHEMA_COMPLEMENTAIRE_CLASSES = {
    name: clas
    for name, clas in inspect.getmembers(ClassTram, inspect.isclass)
    if clas.__module__ == ClassTram.__name__
}
Shema_complémentaire_struct = model.with_structured_output(SHEMA_COMPLEMENTAIRE_CLASSES[struct_roman["schema_complementaire"]])

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer les shema narratif secondaire de l'histoire sous la forme d'un {struct_roman['schema_complementaire']}."),
    SystemMessage(content=f"La structure du roman est la suivante : {struct_roman}"),
    SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Shema narratif principal de l'histoire : {Shema_narratif_principal}"),
    HumanMessage(content=f"Ecrit un shema narratif secondaire, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
]

Shema_complémentaire_narratif = Shema_complémentaire_struct.invoke(message).model_dump()
print(Shema_complémentaire_narratif, "\n\nSchéma narratif complémentaire généré avec succès !")

# Génération des chapitres avec une description pour chaque chapitre

class ChapitreClass(BaseModel):
    titre: str = Field(description="Le titre du chapitre")
    description: str = Field(description="Une courte description de, 3 à 4 lignes de ce qui va se passer dans le chapitre")

class ListeChapitres(BaseModel):
    """Une liste de chapitres pour le roman"""
    chapitres: List[ChapitreClass] = Field(description="Liste des chapitres du roman avec titre et description")

Chapitres_struct = model.with_structured_output(ListeChapitres)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content="Ta mission est de générer la liste des chapitres du roman. Pour chaque chapitre, donne un titre et une description de quelques lignes expliquant ce qui va se passer dans le chapitre."),
    SystemMessage(content=f"Nombre de chapitres: {struct_roman['nombre_chapitres']}"),
    SystemMessage(content=f"Structure du roman : {struct_roman}"),
    SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
    SystemMessage(content=f"Schéma narratif complémentaire de l'histoire : {Shema_complémentaire_narratif}"),
    SystemMessage(content=f"Liste des personnages : {PersonnageDict}"),
    HumanMessage(content="Génère la liste complète des chapitres du roman avec une description de quelques lignes pour chaque chapitre.")
]

Chapitres = Chapitres_struct.invoke(message).model_dump()
ChapitresPourMarkdown = { i + 1: chapitre for i, chapitre in enumerate(Chapitres['chapitres']) } # Je met comme clé le numéro du chapitre pour faciliter la génération du markdown
print(ChapitresPourMarkdown, "\n\nListe des chapitres générée avec succès !\n\n")

# Génération du titre du roman

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content="Ta mission est de générer le titre du roman."),
    SystemMessage(content=f"Structure du roman : {struct_roman}"),
    SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Schéma narratif principal de l'histoire : {Shema_narratif_principal}"),
    SystemMessage(content=f"Schéma narratif complémentaire de l'histoire : {Shema_complémentaire_narratif}"),
    SystemMessage(content=f"Liste des personnages : {PersonnageDict}"),
    SystemMessage(content=f"Liste des chapitres : {Chapitres}"),
    HumanMessage(content="Propose un titre original et accrocheur pour ce roman.")
]

Titre = model.invoke(message).content
print(Titre, "\n\nTitre du roman généré avec succès !")

# Génération du roman complet