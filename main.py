from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

# Obter as variáveis de ambiente do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_KEY = os.getenv("DATABASE_KEY")

# Criar o cliente Supabase
supabase = create_client(DATABASE_URL, DATABASE_KEY)
import logging

app = FastAPI()

# Rota para registrar um usuário
@app.post("/registrar_usuario")
async def register_user(username: str = Form(...), password: str = Form(...)):
    try:
        # Adicione logs para depuração
        logger.info(f"Tentativa de registro de usuário: {username}")

        # Inserir usuário no banco de dados Supabase
        data = await supabase.table("usuarios").insert({"username": username, "password": password})
        if data["error"]:
            raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {str(e)}")
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
        # Excluir usuário do banco de dados Supabase
        data = await supabase.table("usuarios").delete().eq("id", user_id)
        if data["error"]:
            raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")
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