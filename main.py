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

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros.",
    version="1.0.0",
    contact={
        "name":"Lucas Ribeiro",
        "email":"lucasribeirodasilva@gmail.com"
    }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admmin"

security = HTTPBasic()

meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )

@app.get("/")
def hello_world():
    return{"Hello": "World"}

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(security)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos!!!")

    if not meus_livrozinhos:
        return {"message": "Não existe nenhum livro!!!"}

    livros_ordenados = sorted(meus_livrozinhos.items(), key=lambda x: x[0])

    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano livro": livro_data["ano_livro"]}
        for id_livro, livro_data in livros_ordenados[start:end]
    ]

    return {
        "page": page,
        "limit": limit,
        "total": len(meus_livrozinhos),
        "livros": livros_paginados
    }
    

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(security)):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse livro já existe, meu parceiro!")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "O livro foi criado com sucesso!"}
    
@app.put("/livros/{id_livro}")
def atualizar_livro(id_livro: int, livro: Livro):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    meus_livrozinhos[id_livro] = livro.dict()
    return {"message": "Livro atualizado com sucesso!"}
    

@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(security)):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]

        return {"message": "Seu livro foi deletado com sucesso!"}