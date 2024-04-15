from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

# Obter as variáveis de ambiente do arquivo .env
DATABASE_URL = os.getenv("ebdunda1_URL")
DATABASE_KEY = os.getenv("ebdunda1_PASSWORD")

# Criar o cliente Supabase
supabase = create_client(DATABASE_URL, DATABASE_KEY)

app = FastAPI()

# Rota para registrar um usuário
@app.post("/inserir_usuario")
async def inserir_usuario(some_column: str = Form(...), other_column: str = Form(...)):
    try:
        # Inserir novo usuário na tabela 'usuarios' do banco de dados Supabase
        response = await supabase.from_("usuarios").insert([
            {"some_column": some_column, "other_column": other_column}
        ]).execute()

        # Verificar se houve algum erro na inserção
        if response.error:
            raise HTTPException(status_code=500, detail="Erro ao inserir usuário no banco de dados.")

        # Selecionar e retornar os dados inseridos
        inserted_data = await supabase.from_("usuarios").select("*").execute()
        return JSONResponse(content=inserted_data.data)

    except Exception as e:
        print(f"Erro ao inserir usuário no banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao inserir usuário no banco de dados.")

# Rota para listar os usuários cadastrados
@app.get("/usuarios")
async def listar_usuarios():
    try:
        # Consultar os usuários no banco de dados Supabase
        response = await supabase.from_("usuarios").select("*").execute()
        if response.error:
            raise HTTPException(status_code=500, detail="Erro ao obter usuários do banco de dados.")

        # Retornar os usuários como uma resposta JSON
        return JSONResponse(content=response.data)
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