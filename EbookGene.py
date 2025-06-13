import getpass
import os
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

#Génération du monde ou se passe l'histoire

monde_struct = model.with_structured_output(ClassMonde.Monde)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer un monde fictif où l'histoire prend places"),
    SystemMessage(content=f"Tu dois prendre en compte la structure suivante : {struct_roman}")
]

Monde = monde_struct.invoke(message).model_dump()
print(Monde)

#Génération de l'intrigue principal


#Génération du shema narratif principal

Shema_struct = model.with_structured_output(ClassTram.struct_roman["schema_principal"])

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer un {struct_roman["schema_principal"]}"),
    SystemMessage(content=f"La structure du roman est la suivante: {struct_roman}"),
    SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
    HumanMessage(content=f"Ecrit le shema narratif principal, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
]

Shema_narratif_principal = Shema_struct.invoke(message).model_dump()
print(Shema_narratif_principal)

#Génération des personnages

Pers_struct = model.with_structured_output(ClassPers.ListePersonnages)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content="Ta mission est de générer des personnages cohérents avec l'univers donné."),
    SystemMessage(content=f"Structure du roman : {struct_roman}"),
    SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
    HumanMessage(content="Génère un personnage principal, selon les besoins entre 3 et 5 personnages secondaires majeurs et entre 1 et 5 personnages secondaires mineurs")
]

PersonnageDict = Pers_struct.invoke(message).model_dump()
print(PersonnageDict)

#Génération du shema narratif complémentaire

Shema_struct = model.with_structured_output(ClassPers.ListePersonnages)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content=f"Ta mission est de générer un {struct_roman["schema_complementaire"]}"),
    SystemMessage(content=f"La structure du roman est la suivante: {struct_roman}"),
    SystemMessage(content=f"Monde ou prend place l'histoire : {Monde}"),
    SystemMessage(content=f"Shema narratif de l'histoire : {Shema_narratif_principal}"),
    HumanMessage(content=f"Ecrit un shema narratif secondaire, n'hésite pas écrire 3 à 5 lignes pour chaque champs de la classe")
]

Shem_narratif = Shema_struct.invoke(message).model_dump()
print(Shem_narratif)

"""
tools=[
    Tool(
        name="Le scenario a utiliser",
        func=scenario,
        description="Le scenario pour construire la trame"
    )
]

agent = initialize_agent(
    tools,
    model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

Trame = agent.run("Génère une trame principale de roman à partir d'un scénario aléatoire.")
"""
