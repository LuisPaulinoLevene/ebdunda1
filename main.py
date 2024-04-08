from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from dotenv import load_dotenv
import asyncpg
from urllib.parse import urlparse

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

app = FastAPI()

# URL de conexão do PostgreSQL
database_url = "postgres://default:************@ep-rough-dawn-a411n5kq.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Parse o URL de conexão
parsed_url = urlparse(database_url)

# Obter informações de conexão do URL
host = parsed_url.hostname
port = parsed_url.port
user = parsed_url.username
password = parsed_url.password
database_name = parsed_url.path.lstrip('/')

# Rota para exibir a página de usuários
@app.get("/usuarios.html")
async def show_users_page():
    return FileResponse("usuarios.html")

# Função para criar a tabela no PostgreSQL
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

# Agora, chame a função create_table para criar a tabela
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
@app.get("/registro")
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

# Rota para a página inicial
@app.get("/", response_class=FileResponse)
async def read_home():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)