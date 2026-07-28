from dotenv import load_dotenv

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

load_dotenv()


class ChatModel:

    def __init__(self):

        llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-3.1-8B-Instruct",
            task="text-generation",
            max_new_tokens=512,
            temperature=0.2
        )

        self.chat = ChatHuggingFace(llm=llm)

    def get_model(self):
        return self.chat