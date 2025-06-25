import os
import base64

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import Tool, initialize_agent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent_types import AgentType
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool

from openai import OpenAI

import GeneTexteEbook
import Struct_Couverture

os.environ["OPENAI_API_KEY"]="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"

openAI = OpenAI()
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
image_data = None

# Création de l'agent avec les outils nécessaires

def PersInfos(input_str=None):
    PromptPersonnage = f"Les différents personnages sont : {GeneTexteEbook.PersonnageDict}."
    return PromptPersonnage
def MondeInfos(input_str=None):
    PromptMonde = f"Le Monde ou prens places l'histoires est : {GeneTexteEbook.Monde}."
    return PromptMonde
def ShemaNarratifInfos(input_str=None):
    PromptShemaNarratif = f" Le shema narratif est le suivant: {GeneTexteEbook.Shema_narratif_principal}."
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
    HumanMessage(content=f"""Le public cible est {GeneTexteEbook.struct_roman['public']}.
    Le titre doit être visible et intégré dans l'image, le titre est: {GeneTexteEbook.Titre}.
    Tu dois également décider du style de dessin et du type de couverture à utiliser pour le livre, pour cela tu devras utiliser les outils suivants: StyleCouverture_tool et StyleDessin_tool.
    Tu mettra la definition de chaque entre parenthèse

    Infos sur le livre:
    C'est un {GeneTexteEbook.struct_roman['format']} qui est écrit sur un ton {GeneTexteEbook.struct_roman['ton']} et d'un genre {GeneTexteEbook.struct_roman['genres']}.
    L'histoire se déroule dans un {GeneTexteEbook.struct_roman['cadre']}.
    """),
]

cover_save_path = "Sauvegarde/cover_base64.txt"

# Génération de la couverture

if os.path.exists(cover_save_path):
    with open(cover_save_path, "r", encoding="utf-8") as f:
        image_base64 = f.read().strip()
    print("🖼️ Cover chargée depuis la sauvegarde !")
else:
    prompt = agent(message)
    print("Début de la réponses :", prompt["output"])

    response = openAI.responses.create(
        model="gpt-4.1-mini",
        input=prompt["output"],
        tools=[
            {
                "type": "image_generation",
                "quality": "low",
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

    if image_data:
        image_base64 = image_data[0]
        with open(cover_save_path, "w", encoding="utf-8") as f:
            f.write(image_base64)
        print("🖼️ Cover générée et sauvegardée !")
    else:
        image_base64 = None
        print("❌ Aucune image générée.")