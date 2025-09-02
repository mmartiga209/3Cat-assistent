import os
import pprint
import time

from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from typing import Optional, List, TypedDict, Literal
from IPython.display import display, Image

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

# Definició resposta esperada
class Response(TypedDict):
    compliment: Literal["Sí", "No", "No aplica"]
    comentari: str

# Definir l'estructura de l'estat
class State(TypedDict):
    article_text: str   # la notícia
    classification: str
    summary: str
    actions: List[str]  # llista d'accions opcionals a activar (part específica)
    pluralisme_result: Optional[Response]  # resposta estructurada del LLM
    diversitat_result: Optional[Response]
    minories_result: Optional[Response]
    paritat_result: Optional[Response]
    compromis_result: Optional[Response]
    veracitat_result: Optional[Response]
    imparcialitat_result: Optional[Response]
    iteration: int   # per controlar les iteracions de l'autoreflexió

# Carreguem les funcions d'anàlisi
from analysis import (
    pluralisme_analysis,
    diversitat_analysis,
    minories_analysis,
    paritat_analysis,
    compromis_analysis,
    veracitat_analysis,
    imparcialitat_analysis,
    selfreflection_analysis,
    classify_article,
)

CLASSIFICACIO = "classificació"
PLURALISME = "pluralisme"
DIVERSITAT = "diversitat"
MINORIES = "minories"
PARITAT = "paritat"
COMPROMIS = "compromis"
VERACITAT = "veracitat"
IMPARCIALITAT = "imparcialitat"
SELFREFLECTION = "auto-reflexió"
RESUM = "resum"    # NO DEFINITIU

# PART ESPECÍFICA (encara no implementada, només estructura)
VIOLENCIA_GENERE = "violència de gènere"
CONFLICTE_BELIC = "conflicte bèl·lic"
POLITICA = "política"
ESPORT = "esport"
CATALUNYA = "catalunya"
PERSONES_GRANS = "persones grans"
CRISI_CLIMATICA = "crisi climàtica"


# Definim els nodes
def classification_node(state: State) -> State:
    text = state["article_text"]
    res = classify_article(text)  # pot ser dict o llista, depèn del teu analysis.py
    actions: List[str] = []

    # Accepta els dos formats comuns:
    #  - {"categoria": ["Violència de gènere", ...]}
    #  - {"actions":   ["Violència de gènere", ...]}
    if isinstance(res, dict):
        actions = res.get("categoria") or res.get("actions") or []
    elif isinstance(res, list):
        actions = res
    elif isinstance(res, str):
        actions = [res]

    # Assegura tipus final correcte
    actions = [str(a) for a in actions]

    return {"actions": actions}

def pluralisme_node(state: State) -> State:
    text = state["article_text"]
    pluralisme_result = pluralisme_analysis(text)
    return {"pluralisme_result": pluralisme_result}

def diversitat_node(state: State) -> State:
    text = state["article_text"]
    diversitat_result = diversitat_analysis(text)
    return {"diversitat_result": diversitat_result}

def minories_node(state: State) -> State:
    text = state["article_text"]
    minories_result = minories_analysis(text)
    return {"minories_result": minories_result}

def paritat_node(state: State) -> State:
    text = state["article_text"]
    paritat_result = paritat_analysis(text)
    return {"paritat_result": paritat_result}

def compromis_node(state: State) -> State:
    text = state["article_text"]
    compromis_result = compromis_analysis(text)
    return {"compromis_result": compromis_result}

def veracitat_node(state: State) -> State:
    text = state["article_text"]
    veracitat_result = veracitat_analysis(text)
    return {"veracitat_result": veracitat_result}

def imparcialitat_node(state: State) -> State:
    text = state["article_text"]
    imparcialitat_result = imparcialitat_analysis(text)
    return {"imparcialitat_result": imparcialitat_result}

def violencia_genere_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per violència de gènere
    # De moment només retornem un placeholder
    return {}

def conflicte_belic_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per conflicte bèl·lic
    # De moment només retornem un placeholder
    return {}

def politica_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per política
    # De moment només retornem un placeholder
    return {}

def esport_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per esport
    # De moment només retornem un placeholder
    return {}

def catalunya_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per Catalunya
    # De moment només retornem un placeholder
    return {}

def persones_grans_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per persones grans
    # De moment només retornem un placeholder
    return {}

def crisi_climatica_node(state: State) -> State:
    text = state["article_text"]
    # Aquí aniria la funció específica per crisi climàtica
    # De moment només retornem un placeholder
    return {}

def resum_node(state: State) -> State:
    text = state["article_text"]
    # Recopilem els resultats
    results = {}
    results.update(state['pluralisme_result'])
    results.update(state['diversitat_result'])
    results.update(state['minories_result'])
    results.update(state['paritat_result'])
    results.update(state['compromis_result'])
    results.update(state['veracitat_result'])
    results.update(state['imparcialitat_result'])

    resposta_meta = selfreflection_analysis(text, results)
    print(resposta_meta)

    compliment = resposta_meta.get("compliment", "No") if isinstance(resposta_meta, dict) else "No"
    comentari = resposta_meta.get("comentari", "") if isinstance(resposta_meta, dict) else str(resposta_meta)

    # Guardem resum i incrementem iteració
    iteration = state.get("iteration", 0) + 1
    return {
        "summary": f'{{"compliment": "{compliment}", "comentari": "{comentari}"}}',
        "iteration": iteration,
        "classification": compliment,   # guardem per fer routing
    }

# Funció de routing condicional
def decideix_proper_node(state: State) -> str:
    compliment = state.get("classification", "No")
    iteration = state.get("iteration", 0)

    if compliment == "Sí":
        return END
    if iteration >= 2:   # tall de seguretat
        return END
    return PLURALISME    # tornar a l'inici

# Per la part específica
def route(state: State) -> str:
    routes = []
    actions = state.get("actions", [])
    for action in actions:
        if action in routes:
            routes.append(routes[action])
    return routes

# Construcció del workflow
workflow = StateGraph(State)
workflow.add_node(CLASSIFICACIO, classification_node)
workflow.add_node(PLURALISME, pluralisme_node)
workflow.add_node(DIVERSITAT, diversitat_node)
workflow.add_node(MINORIES, minories_node)
workflow.add_node(PARITAT, paritat_node)
workflow.add_node(COMPROMIS, compromis_node)
workflow.add_node(VERACITAT, veracitat_node)
workflow.add_node(IMPARCIALITAT, imparcialitat_node)
workflow.add_node(RESUM, resum_node)
workflow.add_node(VIOLENCIA_GENERE, violencia_genere_node)
workflow.add_node(CONFLICTE_BELIC, conflicte_belic_node)
workflow.add_node(POLITICA, politica_node)
workflow.add_node(ESPORT, esport_node)
workflow.add_node(CATALUNYA, catalunya_node)
workflow.add_node(PERSONES_GRANS, persones_grans_node)
workflow.add_node(CRISI_CLIMATICA, crisi_climatica_node)

workflow.set_entry_point(CLASSIFICACIO)
workflow.add_edge(CLASSIFICACIO, PLURALISME)  # sempre anem a pluralisme després de classificació, paralel·lament s'activaran les parts específiques
workflow.add_edge(PLURALISME, DIVERSITAT)
workflow.add_edge(DIVERSITAT, MINORIES)
workflow.add_edge(MINORIES, PARITAT)
workflow.add_edge(PARITAT, COMPROMIS)
workflow.add_edge(COMPROMIS, VERACITAT)
workflow.add_edge(VERACITAT, IMPARCIALITAT)
workflow.add_edge(IMPARCIALITAT, RESUM)

# Aquí fem l’edge condicional
workflow.add_conditional_edges(
    RESUM,
    decideix_proper_node,
    {PLURALISME: PLURALISME, END: END}
)

workflow.add_conditional_edges(
    CLASSIFICACIO,
    lambda state: state["actions"],
    {
        "Violència de gènere": VIOLENCIA_GENERE,
        "Conflicte bèl·lic": CONFLICTE_BELIC,
        "Política": POLITICA,
        "Esport": ESPORT,
        "Catalunya": CATALUNYA,
        "Persones grans": PERSONES_GRANS,
        "Crisi climàtica": CRISI_CLIMATICA,
    } 
)

# Definir the graph
journalist_assistant = workflow.compile()

# Guardar el graph
png_bytes = journalist_assistant.get_graph().draw_mermaid_png()
with open("images/workflow.png", "wb") as f:
    f.write(png_bytes)

article_prova = """
L'OTAN estima que el 2025 Espanya destinarà el 2% de la despesa del PIB a defensa. Això suposa que, per primer cop, l'estat espanyol complirà amb l'objectiu que els membres de l'organització militar van acordar el 2014 per a la dècada posterior.

D'aquesta manera, el govern espanyol assoleix la xifra promesa l'abril passat per Pedro Sánchez. "Espanya complirà aquest any, 2025, amb el 2% del PIB en defensa", va assegurar el president del govern espanyol en una compareixença posterior al Consell de Ministres a La Moncloa. 

Segons les xifres fetes públiques aquest dijous per l'Aliança, Espanya ha augmentat la despesa en defensa en un 43,11%, de 22.693 milions d'euros el 2024 a 33.123 milions aquest curs. 

En relació amb la despesa en defensa sobre el PIB, Espanya passarà de gastar un 1,28% el 2024 al 2% estimat per aquest any. 

En un comunicat, l'OTAN ha assenyalat que es tracta de xifres recopilades fins al 3 de juny d'aquest any i estima que tots els països membres ja compleixen l'objectiu de despesa del 2% acordat a la cimera de Gal·les del 2014 de cara a la dècada posterior. 

L'any passat només 19 dels 31 arribaven a aquesta fita, segons dades de l'Aliança. 



El Ministeri de Defensa espanyol ha destacat que el compliment d'aquest compromís d'assolir el 2% del PIB d'inversions en l'àmbit de defensa, demostra que Espanya és un "soci fiable i responsable". 

Tot i aquest increment, Espanya es manté, juntament amb Bèlgica, la República Txeca, Luxemburg i Portugal --tots situats també en el 2%--, entre els estats membres de l'OTAN que destinen una proporció més petita del seu PIB a l'àmbit militar. 


Encara lluny del 5% fixat per al 2035 
Pressionats pel president dels Estats Units, Donald Trump, i pels avenços russos al front militar a Ucraïna, els països de l'OTAN van acordar al juny un increment notable de la despesa militar fins al 5% del seu PIB des d'ara fins al 2035. 

Una xifra a la qual no es va comprometre el govern espanyol perquè, tal com va indicar Pedro Sánchez al juny després de la cimera de l'organització, dedicar-hi el 5% del PIB implicaria fer retallades en altres partides com sanitat o pensions, i suposaria una situació "incompatible amb el manteniment de l'estat del benestar i amb la nostra visió del món". 

Tot i que La Moncloa va anunciar un acord amb l'OTAN perquè Espanya no augmentés la despesa militar per sobre del 2,1%, el secretari general de l'Aliança, Mark Rutte, va contradir Sánchez, va negar que hi hagués cap "acord paral·lel" amb Espanya i va afirmar que hauria de fer esforços per assolir el 3,5% acordat estrictament en despesa militar. 

En aquest percentatge s'inclouen aspectes com la compres d'armes, el pagament dels salaris i pensions de les forces armades, missions i maniobres o investigació.

A més, també es va acordar que els estats membres hauran de gastar un 1,5% addicional del PIB en altres aspectes vinculats a la seguretat.
"""

report = journalist_assistant.invoke(
    {
        "article_text": article_prova,
    }
)


