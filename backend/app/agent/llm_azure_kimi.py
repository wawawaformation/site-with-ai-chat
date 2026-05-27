"""
Configuration du LLM  kimi azure
"""

import os
from dotenv import load_dotenv
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

load_dotenv() 



llm = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_AI_INFERENCE_ENDPOINT"),
    model=os.getenv("AZURE_AI_INFERENCE_MODEL"),
    credential=os.getenv("AZURE_AI_INFERENCE_API_KEY"),
)