from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

# Obter as variáveis de ambiente do arquivo .env
DATABASE_URL = os.getenv("ebdunda1_URL")
DATABASE_USER = os.getenv("ebdunda1_USER")
DATABASE_PASSWORD = os.getenv("ebdunda1_PASSWORD")
DATABASE_HOST = os.getenv("ebdunda1_HOST")
DATABASE_NAME = os.getenv("ebdunda1_DATABASE")

app = FastAPI()

# Função para conectar ao banco de dados PostgreSQL
async def connect_to_db():
    return await asyncpg.connect(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        database=DATABASE_NAME
    )

# Rota para registrar um usuário
@app.post("/inserir_usuario")
async def inserir_usuario(username: str = Form(...), password: str = Form(...)):
    try:
        # Conectar ao banco de dados
        conn = await connect_to_db()

        # Inserir novo usuário na tabela 'usuarios' do banco de dados PostgreSQL
        query = "INSERT INTO usuarios (username, password) VALUES ($1, $2) RETURNING id;"
        user_id = await conn.fetchval(query, username, password)

        # Fechar a conexão com o banco de dados
        await conn.close()

        return JSONResponse(content={"user_id": user_id})
    except Exception as e:
        print(f"Erro ao inserir usuário no banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao inserir usuário no banco de dados.")

# Rota para listar os usuários cadastrados
@app.get("/usuarios")
async def listar_usuarios():
    try:
        # Conectar ao banco de dados
        conn = await connect_to_db()

        # Consultar os usuários na tabela 'usuarios' do banco de dados PostgreSQL
        query = "SELECT * FROM usuarios;"
        usuarios = await conn.fetch(query)

        # Fechar a conexão com o banco de dados
        await conn.close()

        return JSONResponse(content=usuarios)
    except Exception as e:
        print(f"Erro ao obter usuários do banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao obter usuários do banco de dados.")

# Rota para a página inicial
@app.get("/", response_class=FileResponse)
async def read_home():
    return FileResponse("index.html")