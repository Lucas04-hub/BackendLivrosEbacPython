Tarefa de livros Python EBAC

API de Livros com Redis

Este projeto é uma API para gerenciar um catálogo de livros, desenvolvida em Python com FastAPI e utilizando Redis para otimização de performance via cache.

Pré-requisitos

Python 3.8+
Poetry instalado
Docker (opcional, para subir o Redis via container)
Redis rodando localmente OU via Docker
Instalação

Clone o repositório

git clone <url-do-repo>
cd backend-livros-ebac-python
Instale as dependências com Poetry

poetry install
Como iniciar o Redis

Opção 1: Usando Docker (Recomendado)

Se você tem o Docker instalado, basta rodar:

docker run --name redis -p 6379:6379 -d redis
O Redis estará disponível em localhost:6379.
Opção 2: Instalação local

Você pode instalar o Redis em sua máquina seguindo as instruções do site redis.io.

Após a instalação, inicie o Redis com:

redis-server
Configuração de variáveis de ambiente

Crie um arquivo .env na raiz do projeto com os seguintes conteúdos:

MEU_USUARIO=seu_usuario
MINHA_SENHA=sua_senha
DATABASE_URL=sqlite:///./livrosdb
Rodando a aplicação

Inicie a aplicação com:

poetry run uvicorn main:app --reload
A documentação interativa estará disponível em:
http://localhost:8000/docs

Funcionalidades

CRUD de livros
Autenticação básica por usuário e senha
Cache de resultados com Redis para maior performance