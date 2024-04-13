from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

# Obter as variáveis de ambiente do arquivo .env
DATABASE_URL = "https://aazeusxcozadmuqqeksz.supabase.co"
DATABASE_KEY = os.getenv("DATABASE_KEY")

# Criar o cliente Supabase
supabase = create_client(DATABASE_URL, DATABASE_KEY)

app = FastAPI()

# Rota para registrar um usuário
@app.post("/registrar_usuario")
async def register_user(username: str = Form(...), password: str = Form(...)):
    try:
        # Inserir usuário no banco de dados Supabase
        data = await supabase.table("usuarios").insert({"username": username, "password": password})
        if data["error"] is not None:
            raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    except Exception as e:
        # Use print para mostrar o erro no console, ou configure o logger
        print(f"Erro ao registrar usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    return RedirectResponse("/usuarios.html")

# Rota para listar os usuários cadastrados
@app.get("/usuarios")
async def listar_usuarios():
    try:
        # Consultar os usuários no banco de dados Supabase
        response = await supabase.table("usuarios").select("*").execute()
        if response["error"]:
            raise HTTPException(status_code=500, detail="Erro ao obter usuários do banco de dados.")

        # Retornar os usuários como uma resposta JSON
        return JSONResponse(content=response["data"])
    except Exception as e:
        print(f"Erro ao obter usuários do banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao obter usuários do banco de dados.")

# Rota para excluir um usuário
@app.delete("/apagar_usuario/{user_id}")
async def delete_usuario(user_id: int):
    try:
        # Excluir usuário do banco de dados Supabase
        data = await supabase.table("usuarios").delete().eq("id", user_id)
        if data["error"]:
            raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")
    except Exception as e:
        print(f"Erro ao excluir o usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")
    return RedirectResponse("/usuarios.html")

# Rota para a página inicial
@app.get("/", response_class=FileResponse)
async def read_home():
    return FileResponse("index.html")