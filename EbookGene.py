import getpass
import os
import categorie
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import Tool, initialize_agent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent_types import AgentType
import categorie
import ClassPers

os.environ["LANGSMITH_TRACING"] = "true"
if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = "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"
if "LANDSMITH_PROJECT" not in os.environ:
    os.environ["LANGSMITH_PROJECT"]="default"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"]="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"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

scenario=categorie.tirer_scenario()

#Génération de la Trame, en 5 lignes

message = [
    SystemMessage("Ecrit la trame principal en un paragraphe de 5 lignes maximum"),
    HumanMessage(f"Ecrit une trame pour ce scenario : {scenario}")
]

Trame = model.invoke(message).content
print(Trame)

#Génération des personnages

Pers_struct = model.with_structured_output(ClassPers.ListePersonnages)

message = [
    SystemMessage(content="Tu es un assistant narratif spécialisé en fiction."),
    SystemMessage(content="Ta mission est de générer des personnages cohérents avec l'univers donné."),
    SystemMessage(content=f"Scenario : {scenario}"),
    SystemMessage(content=f"Trame : {Trame}"),
    HumanMessage(content="Génère un personnage principal, selon les besoins entre 3 et 5 personnages secondaires majeurs et entre 1 et 5 personnages secondaires mineurs")
]

PersonnageDict = Pers_struct.invoke(message).model_dump()
print(PersonnageDict)

#Génération du scenario des péripécie

message = [
    
]

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
