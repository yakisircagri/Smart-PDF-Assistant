from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from services.langfuse_service import langfuse

from dotenv import load_dotenv

load_dotenv()



llm = ChatOpenAI( model = "gpt-4.1-mini")

langfuse_prompt = langfuse.get_prompt(
    "Router prompt"
)

prompt = ChatPromptTemplate.from_template(
    langfuse_prompt.prompt,
    template_format = "mustache"
)

router_chain = prompt | llm |StrOutputParser()



def route_query(query : str):

    decision = router_chain.invoke({"query" : query})

    return decision.strip().lower()