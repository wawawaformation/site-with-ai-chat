"""
-> switch apertus de infomaniak
"""

import os
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_openai import ChatOpenAI

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"La variable d'environnement {name} est manquante")

    return value


infomaniak_endpoint = get_required_env("INFOMANIAK_ENDPOINT")
infomaniak_model = get_required_env("INFOMANIAK_MODEL")
infomaniak_api_key = SecretStr(get_required_env("INFOMANIAK_API_KEY"))

print(infomaniak_endpoint, infomaniak_model)

llm = ChatOpenAI(
    base_url=infomaniak_endpoint,
    model=infomaniak_model,
    api_key=infomaniak_api_key,
    temperature=0.2,
)