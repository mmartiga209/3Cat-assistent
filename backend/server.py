    import os
    import pprint
    import time
    from pathlib import Path
    from functools import lru_cache
    from dotenv import load_dotenv
    from typing import Optional, List, TypedDict
    from duckduckgo_search import DDGS
    from IPython.display import display, Image
    import json


    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain_community.document_loaders import WebBaseLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.document_transformers import BeautifulSoupTransformer

    from langgraph.graph import StateGraph, END

    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Dict

    # Initialize FastAPI App
    app = FastAPI()

    # Enable CORS for frontend requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins (change this for production)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Define Pydantic model for request validation
    class NewsRequest(BaseModel):
        text: str

    # We use the model 4o beacuse we want full outputs
    llm = ChatOpenAI(model="gpt-4o", temperature=0)



    def start():
        # Load environment variables
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

        # Define the data path
        data_path = Path(os.getcwd()).parent / "data"

        # Duckduckgo search
        ddgs = DDGS()


    template1 = '''
    El següent és un article de notícies. Llegeix-lo i realitza la tasca que segueix.

    ####################


    {text}


    ####################

    El següent és un llibre d'estil per a la redacció de notícies. 

    ####################


    {guidelines}


    ####################

    Tasca: Determina si la notícia s'adhereix al llibre d'estil i justifica-ho.

    Instruccions:

    1. Instrucció: Proporciona un paràgraf curt que resumeixi de quina manera l'article està alineat o no amb la guia d'estil. 
    Clau: "reason"
    Valor: Un paràgraf de text en català.

    2. Instrucció: Proporciona un número de 1 a 100, amb 1 indicant molt desalineat i 100 indicant molt alineat.
    Clau: "rating"
    Valor: Un número enter de 1 a 100.

    No retornis res excepte l'objecte JSON de parells clau-valor com a sortida. No retornis markdown.

    '''

    template2 = '''
    El següent és un article de notícies. Llegeix-lo i realitza la tasca que segueix. Respon amb un objecte JSON amb parells clau-valor.


    ####################


    {text}


    ####################


    Tasca: Determina el to general de l'article. És negatiu, positiu o neutral?

    Instrucció: Proporciona un paràgraf curt resumint de quina manera l'article té un to negatiu o positiu.
    Clau: "reason"
    Valor: Un paràgraf de text.

    Instrucció: Proporciona un nombre del -5 al 5, on -5 indica un to molt negatiu i 5 indica un to molt positiu. Un valor de 0 indica que l'article té un to neutral.
    Clau: "rating"
    Valor: Un nombre enter del -5 al 5.

    No retornis res excepte l'objecte JSON de parells clau-valor com a sortida. No retornis markdown.
    '''

    template3 = '''
    El següent és un article de notícies sobre violència masclista. Llegeix-lo i realitza la tasca que segueix.

    ####################


    {text}


    ####################

    El següent és un decàleg sobre el tractament de la violència masclista en notícies.

    ####################


    {guidelines}


    ####################

    Tasca: Determina si la notícia s'adhereix al decàleg i justifica-ho.

    Instruccions:

    1. Instrucció: Proporciona un paràgraf curt que resumeixi de quina manera l'article està alineat o no amb la guia d'estil. 
    Clau: "reason"
    Valor: Un paràgraf de text en català.

    2. Instrucció: Proporciona un número de 1 a 100, amb 1 indicant molt desalineat i 100 indicant molt alineat.
    Clau: "rating"
    Valor: Un número enter de 1 a 100.

    No retornis res excepte l'objecte JSON de parells clau-valor com a sortida. No retornis markdown.

    '''

    # Carreguem el resum del llibre d'estil
    with open('resum.txt', 'r') as file:
        llibre_estil = file.read()

    template1 = template1.replace("{guidelines}", llibre_estil)

    with open('decaleg_violencia_genere.txt', 'r') as file:
        decaleg_violencia = file.read()
        
    template3 = template3.replace("{guidelines}", decaleg_violencia)


    guia_estil_prompt = PromptTemplate(
        input_variables=["text"],
        template=template1
    )

    guia_estil_pipeline = guia_estil_prompt | llm

    tone_analysis_prompt = PromptTemplate(
        input_variables=["text"],
        template=template2
    )

    tone_pipeline = tone_analysis_prompt | llm


    violencia_masclista_prompt = PromptTemplate(
        input_variables=["text"],
        template=template3
    )

    violencia_masclista_pipeline = violencia_masclista_prompt | llm


    def check_guia_estil(article_text: str):
        """
        Summarizes a short article without chunking or combining.
        """
        result = guia_estil_pipeline.invoke({"text": article_text})
        return result.content


    def tone_analysis_article(article_text: str):
        """
        Analyze the tones of the given article text.
        """
        
        tone_result = tone_pipeline.invoke({"text": article_text})
        
        return tone_result.content

    def violencia_masclista(article_text: str):
        """
        Analyze the tones of the given article text.
        """
        
        result = violencia_masclista_pipeline.invoke({"text": article_text})
        
        return result.content


    # Exemple post
    # Define API endpoint to process news text
    @app.post("/pregunta1")
    async def process_text(request: NewsRequest):
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Falta la notícia")
        
        summary_result = check_guia_estil(request.text)

        # convert the string result to a dictionary
        summary_dict = json.loads(summary_result)
        
        return summary_dict

    @app.post("/pregunta2")
    async def process_text(request: NewsRequest):
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Falta la notícia")
        
        summary_result = tone_analysis_article(request.text)

        # convert the string result to a dictionary
        summary_dict = json.loads(summary_result)
        
        return summary_dict


    @app.post("/pregunta3")
    async def process_text(request: NewsRequest):
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Falta la notícia")
        
        summary_result = violencia_masclista(request.text)

        # convert the string result to a dictionary
        summary_dict = json.loads(summary_result)
        
        return summary_dict


    # Run the FastAPI server
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=5000)

