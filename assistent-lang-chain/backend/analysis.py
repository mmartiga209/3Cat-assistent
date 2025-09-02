# analysis.py
from typing import TypedDict, Literal, List
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Model
llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# Definició resposta esperada
class Response(TypedDict):
    compliment: Literal["Sí", "No", "No aplica"]
    comentari: str

class BasicResponse(TypedDict):
    compliment: Literal["Sí", "No"]
    comentari: str

class Classification(TypedDict):
    actions: List[str]



# Noms i fitxers dels criteris
criteris = [
    "pluralisme",
    "diversitat",
    "minories",
    "paritat",
    "compromis",
    "veracitat",
    "imparcialitat",
]

# Carregar prompts i crear pipelines
pipelines = {}
for i, criteri in enumerate(criteris, start=1):
    with open(f"prompts/prompt{i}.txt", "r", encoding="utf-8") as f:
        template = f.read()
    prompt = PromptTemplate(input_variables=["text"], template=template)
    pipelines[criteri] = prompt | llm.with_structured_output(Response)

# Funcions d’anàlisi automàtiques
def run_analysis(criteri: str, article_text: str):
    """
    Executa l’anàlisi per al criteri indicat.
    """
    return pipelines[criteri].invoke({"text": article_text})

# Opcional: alias ràpids (si vols mantenir les funcions individuals)
pluralisme_analysis = lambda text: run_analysis("pluralisme", text)
diversitat_analysis = lambda text: run_analysis("diversitat", text)
minories_analysis   = lambda text: run_analysis("minories", text)
paritat_analysis    = lambda text: run_analysis("paritat", text)
compromis_analysis  = lambda text: run_analysis("compromis", text)
veracitat_analysis  = lambda text: run_analysis("veracitat", text)
imparcialitat_analysis = lambda text: run_analysis("imparcialitat", text)

# Anem a definir la funció d'auto-reflexió
with open(f"prompts/selfreflection.txt", "r", encoding="utf-8") as f:
    selfreflection_template = f.read()

selfreflection_prompt = PromptTemplate(
    input_variables=["text", "respostes"],
    template=selfreflection_template
)
selfreflection_pipeline = selfreflection_prompt | llm.with_structured_output(BasicResponse)

def selfreflection_analysis(article_text: str, results: dict) -> BasicResponse:
    """
    Genera una auto-reflexió basada en els resultats dels altres criteris.
    """
    response = selfreflection_pipeline.invoke({
        "text": article_text,
        "respostes": results
    })

    return response

# Anem a definir el prompt de classificació per temes, per activar les parts específiques
with open(f"prompts/classificacio.txt", "r", encoding="utf-8") as f:
    classification_template = f.read()

classification_prompt = PromptTemplate(
    input_variables=["text"],
    template=classification_template
)

classification_pipeline = classification_prompt | llm.with_structured_output(Classification)

def classify_article(article_text: str) -> Classification:
    """
    Classifica l'article per temes i retorna les accions a activar.
    """
    response = classification_pipeline.invoke({
        "text": article_text
    })

    return response
