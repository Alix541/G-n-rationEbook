import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = "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"
if "LANDSMITH_PROJECT" not in os.environ:
    os.environ["LANGSMITH_PROJECT"]="default"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"]="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"