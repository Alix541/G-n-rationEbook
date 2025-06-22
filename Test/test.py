import json
import sys
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # dossier du script
parent_dir = os.path.abspath(os.path.join(BASE_DIR, '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import ClassTram
import getpass
import inspect
import categorie
import Struct_Couverture

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
import TestEbookPret
from langchain.agents import initialize_agent, Tool

os.environ["OPENAI_API_KEY"]="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"

openAI = OpenAI()
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

print("start")

def PersInfos(input_str=None):
    PromptPersonnage = f"Les différents personnages sont : {TestEbookPret.PersonnageDict}."
    return PromptPersonnage
def MondeInfos(input_str=None):
    PromptMonde = f"Le Monde ou prens places l'histoires est : {TestEbookPret.Monde}."
    return PromptMonde
def ShemaNarratifInfos(input_str=None):
    PromptShemaNarratif = f" Le shema narratif est le suivant: {TestEbookPret.Shema_narratif_principal}."
    return PromptShemaNarratif
def StyleCouverture(input_str=None):
    PromptStyleCouverture = f"Les style de couverture possible sont : {Struct_Couverture.Type_Cover_Def}."
    return PromptStyleCouverture
def StyleDessin(input_str=None):
    PromptStyleCouverture = f"Les style de dessin possible sont : {Struct_Couverture.Style_Dessin_Def}."
    return PromptStyleCouverture

Monde_tool = Tool(
    name="MondeInfos",
    func=MondeInfos,
    description="Donne des informations sur le monde de l'histoire."
)
ShemaNarratif_tool = Tool(
    name="ShemaNarratifInfos",
    func=ShemaNarratifInfos,
    description="Donne des informations sur le schéma narratif de l'histoire."    
)
Personnage_tool = Tool(
    name="PersInfos",
    func=PersInfos,
    description="Donne des informations sur les personnages de l'histoire. Dont le personnage principal, les personnages secondaires majeurs et mineurs."
)
StyleCouverture_tool = Tool(
    name="StyleCouverture",
    func=StyleCouverture,
    description="Donne des informations sur les styles de couverture possibles."
)
StyleDessin_tool = Tool(
    name="StyleDessin",
    func=StyleDessin,
    description="Donne des informations sur les styles de dessin possibles."
)
agent = initialize_agent(
    tools=[Monde_tool,ShemaNarratif_tool,Personnage_tool,StyleCouverture_tool,StyleDessin_tool],
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

message= [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction. Ta mission est de générer un prompt précis et " \
    "étoffer qui dévrit bien l'image de couverture a générer. Ta réponse doit faire au moins une quizaine de ligne, tu doit décrire " \
    "les éléments de décors, les personnages etc.. Utilise bien les outils pour avoir toutes les infos sur les personnages, le mondes etc..."\
    "Tu n'invente rien comme élément de décor que tu n'est pas trouver dans les outils ou le messages utilisaterus"
    ),
    HumanMessage(content=f"""Le public cible est {TestEbookPret.struct_roman['public']}.
    Le titre doit être visible et intégré dans l'image, le titre est: {TestEbookPret.Titre}.
    Tu dois également décider du style de dessin et du type de couverture à utiliser pour le livre, pour cela tu devras utiliser les outils suivants: StyleCouverture_tool et StyleDessin_tool.
    Tu mettra la definition de chaque entre parenthèse

    Infos sur le livre:
    C'est un {TestEbookPret.struct_roman['format']} qui est écrit sur un ton {TestEbookPret.struct_roman['ton']} et d'un genre {TestEbookPret.struct_roman['genres']}.
    L'histoire se déroule dans un {TestEbookPret.struct_roman['cadre']}.
    """),
]

prompt = agent(message)

print("Début de la réponses :", prompt["output"])

response = openAI.responses.create(
    model="gpt-4.1-mini",
    input=prompt["output"],
    tools=[
        {
            "type": "image_generation",
            "quality": "high",
            "size": "1024x1536",
            "output_format": "png",
        }
    ]
)


image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

cover_path = os.path.join(BASE_DIR, "..", "Ebook_Markdown", "cover.png")
cover_path = os.path.abspath(cover_path)

if image_data:
    image_base64 = image_data[0]
    with open(cover_path, "wb") as f:
        f.write(base64.b64decode(image_base64))