from langchain_groq import ChatGroq
from github_ai_agent.config import settings

model = ChatGroq(
    model = "openai/gpt-oss-120b",
    api_key = settings.GROQ_API_KEY
)

if __name__ == '__main__':
    print(model.invoke('hello'))