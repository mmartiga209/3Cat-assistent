# analysis.py
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# We use the model 5 beacuse we want full outputs
llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# Carreguem els prompts
with open("prompts/prompt1.txt", "r", encoding="utf-8") as file:
    prompt1 = file.read()

with open("prompts/prompt2.txt", "r", encoding="utf-8") as file:
    prompt2 = file.read()

with open("prompts/prompt3.txt", "r", encoding="utf-8") as file:
    prompt3 = file.read()



class Response(TypedDict):
    compliment: Literal["Sí", "No", "No aplica"]
    comentari: str

estil_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt1
)

frase_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt2
)

comes_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt3
)


# Pipelines
estil_pipeline = estil_prompt | llm.with_structured_output(Response)
frase_pipeline = frase_prompt | llm.with_structured_output(Response)
comes_pipeline = comes_prompt | llm.with_structured_output(Response)


def estil_analysis(article_text: str):
    """
    Estil verbal.
    """
    result = estil_pipeline.invoke({"text": article_text})
    return result

def frase_analysis(article_text: str):
    """
    Classes de frases.
    """
    result = frase_pipeline.invoke({"text": article_text})
    return result

def comes_analysis(article_text: str):
    """
    Anàlisi de comes.
    """
    result = comes_pipeline.invoke({"text": article_text})
    return result

