import asyncpg
from urllib.parse import urlparse
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

app = FastAPI()

# URL de conexão do PostgreSQL
database_url = "postgres://neondb_owner:sua_senha@ep-lucky-dawn-a5687kqe-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Parse o URL de conexão
parsed_url = urlparse(database_url)

# Obter informações de conexão do URL
host = parsed_url.hostname
port = parsed_url.port
user = parsed_url.username
password = parsed_url.password
database_name = parsed_url.path.lstrip('/')

# Crie uma função para criar a tabela no PostgreSQL
async def create_table():
    conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database=database_name)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    await conn.close()

# Agora, você precisa chamar a função create_table para realmente criar a tabela
create_table()

# Rota para lidar com o formulário de registro de usuário
@app.post("/registrar_usuario")
async def register_user(username: str = Form(...), password: str = Form(...)):
    try:
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database=database_name)
        await conn.execute("INSERT INTO usuarios (username, password) VALUES ($1, $2)", username, password)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    return RedirectResponse("/usuarios.html")

# Rota para mostrar a página de registro de usuário
@app.get("/registro", response_class=HTMLResponse)
async def show_registration_form():
    return FileResponse("registro.html")

# Rota para excluir um usuário
@app.delete("/apagar_usuario/{user_id}")
async def delete_usuario(user_id: int):
    try:
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database=database_name)
        await conn.execute("DELETE FROM usuarios WHERE id = $1", user_id)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")
    return RedirectResponse("/usuarios.html")

# Rota para exibir os usuários
@app.get("/usuarios.html", response_class=HTMLResponse)
async def exibir_usuarios():
    try:
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database=database_name)
        users = await conn.fetch("SELECT * FROM usuarios")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuários.")
    user_rows = ""
    for user in users:
        user_rows += f"<tr><td>{user['id']}</td><td>{user['username']}</td><td>{user['password']}</td><td><form method='post' action='/apagar_usuario/{user['id']}'><button type='submit'>Apagar</button></form></td></tr>"
    return f"<html><body><h1>Usuários</h1><table border='1'><tr><th>ID</th><th>Username</th><th>Password</th><th>Ação</th></tr>{user_rows}</table></body></html>"

# Rota para a página inicial
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request, mensagem: str = None):
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)