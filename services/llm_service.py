from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from langfuse import observe

from services.langfuse_service import langfuse_handler,langfuse

load_dotenv()



langfuse_prompt = langfuse.get_prompt(
    "RAG prompt",
)

prompt = ChatPromptTemplate.from_template(
    langfuse_prompt.prompt,
    template_format = "mustache"
)

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
)

parser = StrOutputParser()

chain = prompt | llm | parser


@observe(name = "generate_answer")
def generate_answer(question,chunks):

    context = "\n\n".join(
        f"page:{chunk['page']}\n{chunk['text']}"
        for chunk in chunks
    )

    answer = chain.invoke({
        "context": context,
        "question": question,
    },
    config = {
            "callbacks" : [langfuse_handler]
        }
    )

    return answer


