import os
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from typing import Optional, List, TypedDict
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
from typing import List, Dict, TypedDict, Literal

# Import analysis functions
from analysis import (
    estil_analysis,
    frase_analysis,
    comes_analysis,
)


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

# We use the model 5 beacuse we want full outputs
llm = ChatOpenAI(model="gpt-5", temperature=1)



def start():
    # Load environment variables
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

    # Define the data path 
    data_path = Path(os.getcwd()).parent / "data"

    setup()




def setup():
    # A aquesta funció carregarem les funcions
    pass






# Exemple post
# Define API endpoint to process news text
@app.post("/analisigeneral")
async def process_text(request: NewsRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Falta la notícia")
    
    # Ara farem els diferents anàlisis per tots els criteris
    results = {}
    results.update(estil_analysis(request.text))
    #results.update(frase_analysis(request.text))
    #results.update(comes_analysis(request.text))
    print(results)
    return results
    

    # Aquí podríem fer un resum de tots els resultats
    # De moment per les proves només retornem el resultat de les prompts individuals
    
    return summary


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

