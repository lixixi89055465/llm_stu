import getpass
import os
import os
from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

print('1'*100)
print(os.environ.get("HTTP_PROXY"))
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")
model.invoke("Hello, world!")

