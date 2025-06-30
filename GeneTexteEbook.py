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

from langgraph.prebuilt import create_openai_functions_agent
from typing import TypedDict

from openai import OpenAI
import base64

import categorie
import ClassPers
import ClassMonde
import ClassTram
from langchain.memory import ConversationBufferMemory

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


messageInitialisation = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est d'écrire un chapitre entier du roman, en respectant la taille indiquée qui est de environ {struct_roman['caracteres_par_chapitre']} caractères."),
    SystemMessage(content="Tu peux t'aider des outils à ta disposition pour accéder à tout élément utile (structure du roman, monde, personnages, schémas narratifs, description du chapitre, shema_complementaire_narratif, etc). N'hésite pas à les utiliser pour garantir la cohérence et la richesse du récit."),
    SystemMessage(content=f"Voici la structure du roman : {struct_roman}"),
    SystemMessage(content=f"Monde où prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Schéma narratif principal (à garder en mémoire) : {Shema_narratif_principal}"),
    SystemMessage(content=f"Schéma narratif complémentaire (à garder en mémoire) : {Shema_complementaire_narratif}"),
    SystemMessage(content=f"Liste des personnages (à garder en mémoire): {PersonnageDict}"),
    SystemMessage(content=f"Résumé rapide de l'idée principale du chapitre à écrire : {ChapitresPourMarkdown['1']['description']}"),
    SystemMessage(content=f"Titre du chapitre a écrire : {ChapitresPourMarkdown['1']['titre']}"),
    SystemMessage(content="N'oublie pas de respecter la cohérence avec les chapitres précédents et d'assurer la continuité de l'intrigue."),
    HumanMessage(content="Écris le chapitre complet.")
]

messageBoucle = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est d'écrire un chapitre entier du roman, en respectant la taille indiquée qui est de environ {struct_roman['caracteres_par_chapitre']} caractères."),
    SystemMessage(content="Tu peux t'aider des outils à ta disposition pour accéder à tout élément utile (structure du roman, monde, personnages, schémas narratifs, description du chapitre, shema_complementaire_narratif, etc). N'hésite pas à les utiliser pour garantir la cohérence et la richesse du récit."),
    SystemMessage(content=f"Résumé rapide de l'idée principale du chapitre à écrire :"),
    SystemMessage(content=f"Titre du chapitre a écrire :") ,
    SystemMessage(content=f"Résumer de l'emsemble des chapitres précédent écrit : "),
    SystemMessage(content="N'oublie pas de respecter la cohérence avec les chapitres précédents et d'assurer la continuité de l'intrigue."),
    HumanMessage(content="Écris le chapitre complet.")
]

class ChapterState(TypedDict, total=False):
    """État du chapitre en cours d'écriture."""
    Index: int  # Index du chapitre (par défaut 1)
    Texte: List[str]
    Recap: List[str]


# Création des outils pour l'agent

def get_struct_roman(input_str=None) -> str:
    """Retourne la structure du roman sous forme de texte JSON formaté."""
    return json.dumps(struct_roman, ensure_ascii=False, indent=2)

def get_monde(input_str=None) -> str:
    """Retourne la description du monde sous forme de texte JSON formaté."""
    return json.dumps(Monde, ensure_ascii=False, indent=2)

def get_shema_narratif_principal(input_str=None) -> str:
    """Retourne le schéma narratif principal sous forme de texte JSON formaté."""
    return json.dumps(Shema_narratif_principal, ensure_ascii=False, indent=2)

def get_shema_complementaire_narratif(input_str=None) -> str:
    """Retourne le schéma narratif complémentaire sous forme de texte JSON formaté."""
    return json.dumps(Shema_complementaire_narratif, ensure_ascii=False, indent=2)

def get_personnages(input_str=None) -> str:
    """Retourne la liste des personnages sous forme de texte JSON formaté."""
    return json.dumps(PersonnageDict, ensure_ascii=False, indent=2)

def get_description_chapitre(nbchap: int = 0) -> str:
    """Retourne la description du chapitre courant."""
    return ChapitresPourMarkdown[nbchap + 1]['description']

def get_Liste_Chap_Deja_Ecrit_Resume(chapitre: ChapterState) -> str:
    """Retourne la description de tous les chapitres précédents écrits."""
    return "\n\n".join([chap["resume"] for chap in chapitre['Recap']])

tools = [
    Tool(
        name="AfficherStructureRoman",
        func=lambda _: get_struct_roman(),
        description="Affiche la structure du roman (struct_roman) au format JSON."
    ),
    Tool(
        name="AfficherMonde",
        func=lambda _: get_monde(),
        description="Affiche la description du monde fictif (Monde) au format JSON."
    ),
    Tool(
        name="AfficherSchemaNarratifPrincipal",
        func=lambda _: get_shema_narratif_principal(),
        description="Affiche le schéma narratif principal (Shema_narratif_principal) au format JSON."
    ),
    Tool(
        name="AfficherSchemaNarratifComplementaire",
        func=lambda _: get_shema_complementaire_narratif(),
        description="Affiche le schéma narratif complémentaire (Shema_complementaire_narratif) au format JSON."
    ),
    Tool(
        name="AfficherPersonnages",
        func=lambda _: get_personnages(),
        description="Affiche la liste des personnages (PersonnageDict) au format JSON."
    ),
    Tool(
        name="AfficherDescriptionChapitre",
        func=lambda x: get_description_chapitre(int(x)),
        description="Affiche la description du chapitre dont le numéro est passé en argument (commence à 0)."
    ),
    Tool(
        name="AfficherDescriptionChapitreDejaEcrit",
        func=lambda _: get_Liste_Chap_Deja_Ecrit_Resume(),
        description="Affiche la liste des résumés de tous les chapitres déjà écrits, pour aider à la continuité de l'histoire."
    ),
]

llm_with_tools = model.bind_tools(tools)

def WriteTexteChapitre(chapitre: ChapterState) -> str:
    """Écrit le texte du chapitre en cours."""
    if chapitre["Index"] == 0:
        msg = llm_with_tools.invoke(messageInitialisation)
    else:
        messageBoucle[3] = SystemMessage(content=f"Résumé rapide de l'idée principale du chapitre à écrire : {ChapitresPourMarkdown[str(chapitre['Index']+1)]['description']}"),
        messageBoucle[4] = SystemMessage(content=f"Titre du chapitre a écrire : {ChapitresPourMarkdown[str(chapitre['Index']+1)]['titre']}"),
        messageBoucle[5] = SystemMessage(content=f"Résumer de l'emsemble des chapitres précédent écrit : {chapitre['Recap']}")
        msg = llm_with_tools.invoke(messageBoucle)
    chapter_text = msg.content
    chapitre["Texte"].append(chapter_text)
    return {"Texte": chapitre["Texte"]}

def WriteRecapChapitre(chapitre: ChapterState) -> str:
    """Écrit le recapitulatif du chapitre en cours."""
    messageRecap = [
        SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
        SystemMessage(content="Ta mission est de générer un récapitulatif du chapitre écrit de 5 lignes grand maximum."),
        HumanMessage(content=f"Voici le chapitre a résumer : {chapitre['Texte'][chapitre['Index']]}"),
    ]
    msg = llm_with_tools.invoke(messageRecap)
    chapitre["Recap"].append(msg.content)
    return {"Recap": chapitre["Recap"]}

def UpIndex(chapitre: ChapterState) -> str:
    """Met à jour l'index du chapitre en cours."""
    chapitre["Index"] += 1
    return {"Index": chapitre["Index"]}

"""
# Ajout de la mémoire pour l'agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory
)

# Sauvegarde des chapitres complets et des résumés
chapitres_texte_path = "Sauvegarde/chapitres_texte.json"
if os.path.exists(chapitres_texte_path):
    with open("Sauvegarde/chapitres_resume.json", "r", encoding="utf-8") as f:
        ChapitrePrecedent = json.load(f)
    print("📖 Chapitres entiers et résumés chargés depuis la sauvegarde !")
else:
    ChapitrePrecedent = []

    # Génération du premier chapitre avec messageInitialisationé
    response = agent.invoke(messageInitialisation)
    chapitre_text = response.content.split("---RESUME---")[0].strip()
    resume_text = response.content.split("---RESUME---")[1].strip() if "---RESUME---" in response.content else ""

    ChapitrePrecedent.append({
        "titre": ChapitresPourMarkdown[1]['titre'],
        "description": ChapitresPourMarkdown[1]['description'],
        "texte": chapitre_text,
        "resume": resume_text
    })
    print(f"Chapitre 1 écrit avec succès !")

    for i in range(1, struct_roman['nombre_chapitres']):
        nbchap = i
        messageBoucle[5] = SystemMessage(content=f"Résumé rapide de l'idée principale du chapitre à écrire : {ChapitresPourMarkdown[str(nbchap+1)]['description']}")
        messageBoucle[6] = SystemMessage(content=f"Titre du chapitre a écrire : {ChapitresPourMarkdown[str(nbchap+1)]['titre']}")
        messageBoucle[7] = SystemMessage(content=f"Résumer de l'emsemble des chapitres précédent écrit : {ChapitrePrecedent[nbchap-1]['resume']}")

        response = agent.invoke(messageBoucle)
        chapitre_text = response.content.split("---RESUME---")[0].strip()
        resume_text = response.content.split("---RESUME---")[1].strip() if "---RESUME---" in response.content else ""

        ChapitrePrecedent.append({
            "titre": ChapitresPourMarkdown[str(nbchap+1)]['titre'],
            "description": ChapitresPourMarkdown[str(nbchap+1)]['description'],
            "texte": chapitre_text,
            "resume": resume_text
        })
        print(f"Chapitre {nbchap+1} écrit avec succès !")

    # Sauvegarde des chapitres complets et des résumés
    with open("Sauvegarde/chapitres_resume.json", "w", encoding="utf-8") as f:
        json.dump(ChapitrePrecedent, f, ensure_ascii=False, indent=2)
    print("📖 Chapitres entiers et résumés sauvegardés !")
"""