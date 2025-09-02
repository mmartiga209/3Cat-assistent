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
    prompt_pluralisme = file.read()

with open("prompts/prompt2.txt", "r", encoding="utf-8") as file:
    prompt_diversitat = file.read()

with open("prompts/prompt3.txt", "r", encoding="utf-8") as file:
    prompt_minories = file.read()

with open("prompts/prompt4.txt", "r", encoding="utf-8") as file:
    prompt_paritat = file.read()

with open("prompts/prompt5.txt", "r", encoding="utf-8") as file:
    prompt_compromis = file.read()

with open("prompts/prompt6.txt", "r", encoding="utf-8") as file:
    prompt_veracitat = file.read()

with open("prompts/prompt7.txt", "r", encoding="utf-8") as file:
    prompt_imparcialitat = file.read()

class Response(TypedDict):
    compliment: Literal["Sí", "No", "No aplica"]
    comentari: str

pluralisme_promt = PromptTemplate(
    input_variables=["text"],
    template=prompt_pluralisme
)

diversitat_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_diversitat
)

minories_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_minories
)

paritat_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_paritat
)

compromis_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_compromis
)

veracitat_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_veracitat
)

imparcialitat_prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_imparcialitat
)

# Pipelines
pluralisme_pipeline = pluralisme_promt | llm.with_structured_output(Response)
diversitat_pipeline = diversitat_prompt | llm.with_structured_output(Response)
minories_pipeline = minories_prompt | llm.with_structured_output(Response)
paritat_pipeline = paritat_prompt | llm.with_structured_output(Response)
compromis_pipeline = compromis_prompt | llm.with_structured_output(Response)
veracitat_pipeline = veracitat_prompt | llm.with_structured_output(Response)
imparcialitat_pipeline = imparcialitat_prompt | llm.with_structured_output(Response)


def pluralisme_analysis(article_text: str):
    """
    Criteri pluralisme.
    """
    result = pluralisme_pipeline.invoke({"text": article_text})
    return result

def diversitat_analysis(article_text: str):
    """
    Criteri diversitat.
    """
    result = diversitat_pipeline.invoke({"text": article_text})
    return result

def minories_analysis(article_text: str):
    """
    Criteri minories.
    """
    result = minories_pipeline.invoke({"text": article_text})
    return result

def paritat_analysis(article_text: str):
    """
    Criteri paritat.
    """
    result = paritat_pipeline.invoke({"text": article_text})
    return result

def compromis_analysis(article_text: str):
    """
    Criteri compromís.
    """
    result = compromis_pipeline.invoke({"text": article_text})
    return result

def veracitat_analysis(article_text: str):
    """
    Criteri veracitat.
    """
    result = veracitat_pipeline.invoke({"text": article_text})
    return result

def imparcialitat_analysis(article_text: str):
    """
    Criteri imparcialitat.
    """
    result = imparcialitat_pipeline.invoke({"text": article_text})
    return result
