from http.client import HTTPException

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import asyncpg
from dotenv import load_dotenv
import os
from pathlib import Path
from starlette.responses import FileResponse, HTMLResponse

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


@app.get("/utilizadores.html", response_class=HTMLResponse)
async def read_utilizadores():
    file_path = Path("templates") / "utilizadores.html"
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


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

        return {"user_id": user_id}
    except Exception as e:
        print(f"Erro ao inserir usuário no banco de dados: {str(e)}")
        raise FastAPI(status_code=500, detail="Erro ao inserir usuário no banco de dados.")

# Rota para listar os usuários cadastrados em formato JSON
@app.get("/usuarios", response_class=HTMLResponse)
async def listar_usuarios():
    try:
        # Conectar ao banco de dados
        conn = await connect_to_db()

        # Consultar os usuários na tabela 'usuarios' do banco de dados PostgreSQL
        query = "SELECT * FROM usuarios;"
        usuarios = await conn.fetch(query)

        # Fechar a conexão com o banco de dados
        await conn.close()

        # Gerar a tabela HTML com os dados dos usuários
        table_html = "<table border='1'><thead><tr><th>ID</th><th>Username</th><th>Password</th></tr></thead><tbody>"
        for usuario in usuarios:
            table_html += f"<tr><td>{usuario['id']}</td><td>{usuario['username']}</td><td>{usuario['password']}</td></tr>"
        table_html += "</tbody></table>"

        # Retornar a tabela HTML com os dados dos usuários
        return table_html
    except Exception as e:
        print(f"Erro ao obter usuários do banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao obter usuários do banco de dados.")


# Rota para a página inicial
@app.get("/", response_class=FileResponse)
async def read_home():
    file_path = Path("templates") / "index.html"
    return FileResponse(file_path, media_type="text/html")