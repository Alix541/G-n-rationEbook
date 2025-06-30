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