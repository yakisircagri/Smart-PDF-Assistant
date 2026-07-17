from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler
from langfuse import get_client

load_dotenv()

langfuse = get_client()

langfuse_handler = CallbackHandler()




