from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

class LLMManager:
    def __init__(self):
        self.llm = ChatDeepSeek(model="deepseek-chat", temperature=0)

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content