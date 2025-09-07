import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.load_config import load_config
from langchain_openai import ChatOpenAI

class LoadConfig:
    def __init__(self):
        print(f"Loaded config...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

class LoadModel(BaseModel):
    model_provider: Literal["openai"] = "openai"
    config: Optional[LoadConfig] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = LoadConfig()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM Model
        """
        print("LLM Loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "openai":
            print("Loading LLM from OpenAI...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)

        return llm