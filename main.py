# API de Livros

# GET, POST, PUT, DELETE

# POST - Adicionar novos Livros (Create)
# GET - Buscar os dados dos Livros (Read)
# PUT - Atualizar informações dos livros (Update)
# DELETE - Deletar informações dos lirvos (Delete)

# CRUD

# Create
# Read
# Update
# Delete

# Vamos acessar nosso ENDPOINT = HTTP
# E vamos acessar os PATH's desse endpoint
# Path = Rota
# Query Strings = Adicionar informações atravez da propria URL inteira

# Documentação Swagger -> Documentar os endpoints da nossa aplicação (da nossa API)

# Olha, acessa minha documentação swagger nesse endpoint -> http://endpointdelivros/docs#/

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os
import redis
import json
from fastapi import BackgroundTasks

from celery_app import celery_app
from celery.result import AsyncResult
from tasks import fatorial, somar

from kafka_producer import enviar_evento

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

import logging.config
import yaml
from elasticsearch import Elasticsearch
from datetime import datetime

import asyncio

from dotenv import load_dotenv
load_dotenv()
DATABSE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABSE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "livros-logos")
es_client = Elasticsearch([ELASTICSEARCH_URL])

#REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
#REDIS_PORT = os.getenv("REDIS_PORT", "6379")
#redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

es = Elasticsearch(hosts=["http://elasticsearch:9200"])
with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.info("API Inicializada com sucesso")

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros.",
    version="1.0.0",
    contact={
        "name":"Lucas Ribeiro",
        "email":"lucasribeirodasilva@gmail.com"
    }
)

# Variaveis de ambiente
security = HTTPBasic()

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    MEU_USUARIO = os.getenv("MEU_USUARIO")
    MINHA_SENHA = os.getenv("MINHA_SENHA")
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

security = HTTPBasic()

meus_livrozinhos = {}

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)

# def salvar_livro_redis(livro_id: int, livro: Livro):
#    redis_client.set(f"livro:{livro_id}", json.dumps(livro.dict()))

# def deletar_livro_redis(livro_id: int):
#    redis_client.delete(f"livro:{livro_id}")



def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    MEU_USUARIO = os.getenv("MEU_USUARIO")
    MINHA_SENHA = os.getenv("MINHA_SENHA")
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@app.get("/")
def hello_world():
    logger.info("Alguém acessou a raiz da API.")
    return{"Hello": "World!"}

async def chamadas_externas_1():
    await asyncio.sleep(2)
    return {"Resultado chamadas_externa_1"}

async def chamadas_externas_2():
    await asyncio.sleep(2)
    return {"Resultado chamadas_externa_2"}

async def chamadas_externas_3():
    await asyncio.sleep(2)
    return {"Resultado chamadas_externa_3"}

@app.get("/chamadas-externas")
async def chamadas_externas():
    tarefa1 = asyncio.create_task(chamadas_externas_1())
    tarefa2 = asyncio.create_task(chamadas_externas_2())
    tarefa3 = asyncio.create_task(chamadas_externas_3())

    resultado1 = await tarefa1
    resultado2 = await tarefa2
    resultado3 = await tarefa3

    return {
        "mensagem": "Todas as chamadas nas API's foram concluidas com sucesso",
        "resultado": [resultado1, resultado2, resultado3]
    }

#@app.post("/calcular/soma")
#def calcular_soma(a: int, b: int):
#    tarefa = somar.delay(a,b)
#    redis_client.lpush("tarefas_ids", tarefa.id)
#    redis_client.ltrim("tarefas_ids", 0, 49)
#    return {
#        "task_id": tarefa.id,
#        "message":"Tarefa de soma enviada para execução!"
#    }

#@app.post("/calcular/fatorial")
#def calcular_fatorial(n: int):
#    try:
#        tarefa = fatorial.delay(n)
#        redis_client.lpush("tarefas_ids", tarefa.id)
#        redis_client.ltrim("tarefas_ids", 0, 49)
#        return {
#            "task_id": tarefa.id,
#            "message": "Tarefa de fatorial enviada para execução!"
#        }
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))



#@app.get("/tarefas/recentes")
#def listar_tarefas_recentes():
#    ids = redis_client.lrange("tarefas_ids", 0, -1)
#    tarefas = []
    
#    for task_id in ids:
#        resultado = AsyncResult(task_id, app=celery_app)
#        tarefas.append({
#            "task_id": task_id,
#            "status": resultado.status,
#            "resultado": resultado.result if resultado.successful() else None
#        })

#    return {
#        "tarefas": tarefas
#    }



# @app.get("/debug/redis")
# def ver_livros_redis():
#    chaves = redis_client.keys("livros:*")
#    livros = []

#    for chave in chaves:
#        valor = redis_client.get(chave)
#        ttl = redis_client.ttl(chave)
#
#        livros.append({"chave": chave, "valor": json.loads(valor), "ttl": ttl})

#    return livros

@app.get("/livros")
def listar_livros(
    page: int = 1, 
    limit: int = 10, 
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos!!!")

    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()

    if not livros:
        response = {"message": "Não existe livro nenhum!!"}
    else:
        total_livros = db.query(LivroDB).count()
        response = {
            "page": page,
            "limit": limit,
            "total": total_livros,
            "livros": [
                {
                    "id": livro.id,
                    "nome_livro": livro.nome_livro,
                    "autor_livro": livro.autor_livro,
                    "ano_livro": livro.ano_livro
                } for livro in livros
            ]
        }

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": "/livros",
        "usuario": credentials.username,
        "page": page,
        "limit": limit,
        "status": "success" if livros else "not_found",
        "total_livros": len(livros)
    }

    try:
        es_client.index(index=ELASTICSEARCH_INDEX, body=log)
    except Exception as e:
        print(f"Erro ao enviar log para o Elasticsearch: {e}")

    return response
    
# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro

@app.post("/livros")
async def post_livros(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(security)):
    db_livro = db.query(LivroDB).filter(
        LivroDB.nome_livro == livro.nome_livro,
        LivroDB.autor_livro == livro.autor_livro
    ).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe dentro do banco de dados!!!")
    novo_livro = LivroDB(
        nome_livro=livro.nome_livro,
        autor_livro=livro.autor_livro,
        ano_livro=livro.ano_livro
    )
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    logger.info({
        "acao": "criar",
        "livro": livro.dict(),
        "livro_id": novo_livro.id
    })

    return {"message": "O livro foi criado com sucesso!"}
    
@app.put("/livros/{id_livro}")
async def atualizar_livro(id_livro: int, livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(security)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")

    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    logger.info({
        "acao": "atualizar",
        "livro_id": id_livro,
        "livro": livro.dict()
    })

    return {"message": "Livro atualizado com sucesso!"}

@app.delete("/livros/{id_livro}")
async def deletar_livro(id_livro: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(security)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    db.delete(db_livro)
    db.commit()

    logger.info({
        "acao": "deletar",
        "livro_id": id_livro,
    })

    return {"message": "Livro removido com sucesso!"}

# ACID
# ORM -> Object Relational Mapping
# FastAPI / Django / Flask / Node / Express / Nest.js / Laravel / Spring Boot -> Frameworks Backends
# Vantagens -> A gente vai ganhar agilidade no desenvolvimento
# Desvantagens -> A gente pode perder performace no Banco de Dados