from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

app = FastAPI()

# Acesse as variáveis de ambiente conforme necessário
database_url = os.getenv("DATABASE_URL")
database_url_unpooled = os.getenv("DATABASE_URL_UNPOOLED")

# Rota para mostrar o URL do banco de dados
@app.get("/database")
async def get_database_url():
    return {"database_url": database_url}

# Rota para mostrar o URL do banco de dados não agrupado
@app.get("/database_unpooled")
async def get_unpooled_database_url():
    return {"database_url_unpooled": database_url_unpooled}

# Rota para lidar com o formulário de registro de usuário
@app.post("/registrar_usuario")
async def register_user(username: str = Form(...), password: str = Form(...)):
    # Aqui você pode adicionar a lógica para registrar o usuário no banco de dados
    # Se ocorrer um erro durante o registro, você pode levantar uma exceção HTTPException
    # Por exemplo:
    # if erro_ocorreu:
    #     raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    return {"username": username, "password": password}

# Rota para mostrar a página de registro de usuário
@app.get("/registro", response_class=HTMLResponse)
async def show_registration_form():
    # Aqui você pode retornar o conteúdo HTML da página de registro
    # Por exemplo:
    # return FileResponse("registro.html")
    return "<html><body><h1>Página de Registro</h1><form method='post' action='/registrar_usuario'><input type='text' name='username' placeholder='Username'><br><input type='password' name='password' placeholder='Password'><br><button type='submit'>Registrar</button></form></body></html>"


# Função para excluir um usuário do banco de dados
async def delete_user(user_id: int):
    try:
        # Conectar ao banco de dados PostgreSQL
        conn = await asyncpg.connect("postgresql://usuario:senha@localhost/nome_do_banco")

        # Excluir o usuário da tabela pelo ID
        await conn.execute("DELETE FROM usuarioss WHERE id = $1", user_id)

        # Fechar a conexão com o banco de dados
        await conn.close()

        # Excluir o usuário do Supabase
        await supabase.table('usuarioss').delete(where='id.eq.' + str(user_id))

        return True

    except Exception as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao excluir o usuário:", e)
        return False

# Rota para excluir um usuário
@app.delete("/apagar_usuario/{user_id}")
async def delete_usuario(user_id: int):
    if await delete_user(user_id):
        return RedirectResponse("/usuarios.html")
    else:
        raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")

# Rota para exibir os usuários
@app.get("/usuarios.html", response_class=HTMLResponse)
async def exibir_usuarios():
    try:
        # Selecionar todos os usuários da tabela
        usuarios = await supabase.table('usuarioss').select()

        # Construir uma tabela HTML para exibir os usuários
        table_content = "<h2>Usuários</h2>"
        table_content += "<table border='1'><tr><th>ID</th><th>Username</th><th>Password</th><th>Ação</th></tr>"
        for usuario in usuarios['data']:
            table_content += f"<tr><td>{usuario['id']}</td><td>{usuario['username']}</td><td>{usuario['password']}</td>"
            table_content += f"<td><form method='post' action='/apagar_usuario/{usuario['id']}'><button type='submit'>Apagar</button></form></td></tr>"
        table_content += "</table>"

        # Retornar a resposta HTML
        return HTMLResponse(content=table_content)

    except Exception as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao buscar os usuários:", e)
        # Levantar uma exceção HTTP 500
        raise HTTPException(status_code=500, detail="Erro ao buscar os usuários. Por favor, tente novamente.")

# Rota para a página inicial
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request, mensagem: str = None):
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)