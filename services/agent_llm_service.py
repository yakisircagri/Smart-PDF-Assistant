from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from agent.prompt import REASON_PROMPT
from services.llm_service import llm

reason_prompt = ChatPromptTemplate(
    [
        ("system", REASON_PROMPT.prompt),
        ("human","{question}")
    ]
)

reason_chain = (
    reason_prompt
    |llm
    |StrOutputParser()
)

def reason(question : str, document_count : int):

    return reason_chain.invoke(
        {
            "question": question,
            "document_count" : document_count
        }
    )


chat_llm = ChatOpenAI(model="gpt-4.1-mini")

chat_prompt = ChatPromptTemplate.from_messages(
[
    (
        "system",
        """
You are a general purpose AI assistant.
Answer the user's question directly and clearly.

Rules:
- If the user asks a general knowledge question, answer it.
- If the user greets you, respond naturally.
- Do not ask what the user needs unless the user only says hello.
"""
    ),
    (
        "human",
        "{question}"
    )
]
)

chat_chain = chat_prompt | chat_llm | StrOutputParser()

def chat_answer(question : str):

    return chat_chain.invoke(
        {
            "question": question
        }
    )