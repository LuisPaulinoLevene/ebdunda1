import sqlite3
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from supabase_py import create_client

app = FastAPI()

# Função para criar todas as tabelas necessárias
def create_usuarioss_table():
    conn = sqlite3.connect("Maquina.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarioss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chamar a função para garantir que a tabela 'usuarioss' seja criada
create_usuarioss_table()

# Configurar o Supabase
supabase_url = "https://ktsnyufwyiqtetkctbfk.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0c255dWZ3eWlxdGV0a2N0YmZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI0OTU5MTQsImV4cCI6MjAyODA3MTkxNH0.5a-L_BpattY7fbsq-iNHOboQr0mLopXLtDk9mubtypE"
supabase = create_client(supabase_url, supabase_key)

# Rota para servir o arquivo HTML de registro
@app.get("/registro", response_class=HTMLResponse)
async def show_registration_form():
    return FileResponse("usuarios.html")

# Rota para processar o formulário de registro
@app.post("/registrar_usuario")
async def register_user(username: str = Form(...), password: str = Form(...)):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect("Maquina.db")
        cursor = conn.cursor()

        # Inserir os dados do usuário na tabela 'usuarioss'
        cursor.execute(
            "INSERT INTO usuarioss (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        # Inserir os dados no Supabase
        supabase.table('usuarioss').insert({"username": username, "password": password})

        # Redirecionar para a página de sucesso (pode ser a mesma página de registro)
        return RedirectResponse(url="/registro")

    except Exception as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao registrar usuário:", e)
        # Retornar uma mensagem de erro ao cliente
        raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")

# Função para excluir um usuário do banco de dados
def delete_user(user_id: int):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect("Maquina.db")
        cursor = conn.cursor()

        # Excluir o usuário da tabela pelo ID
        cursor.execute("DELETE FROM usuarioss WHERE id = ?", (user_id,))
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        # Excluir o usuário do Supabase
        supabase.table('usuarioss').delete(where='id.eq.' + str(user_id))

        return True

    except sqlite3.Error as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao excluir o usuário:", e)
        return False

# Rota para excluir um usuário
@app.delete("/apagar_usuario/{user_id}")
async def delete_usuario(user_id: int):
    if delete_user(user_id):
        return RedirectResponse("/usuarios.html")
    else:
        raise HTTPException(status_code=500, detail="Erro ao excluir o usuário. Por favor, tente novamente.")

# Rota para exibir os usuários
@app.get("/usuarios.html", response_class=HTMLResponse)
async def exibir_usuarios():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect("Maquina.db")
    cursor = conn.cursor()

    try:
        # Selecionar todos os usuários da tabela
        cursor.execute("SELECT * FROM usuarioss")
        usuarios = cursor.fetchall()

        # Fechar a conexão com o banco de dados
        conn.close()

        # Construir uma tabela HTML para exibir os usuários
        table_content = "<h2>Usuários</h2>"
        table_content += "<table border='1'><tr><th>ID</th><th>Username</th><th>Password</th><th>Ação</th></tr>"
        for usuario in usuarios:
            table_content += f"<tr><td>{usuario[0]}</td><td>{usuario[1]}</td><td>{usuario[2]}</td>"
            table_content += f"<td><form method='post' action='/apagar_usuario/{usuario[0]}'><button type='submit'>Apagar</button></form></td></tr>"
        table_content += "</table>"

        # Retornar a resposta HTML
        return HTMLResponse(content=table_content)

    except sqlite3.Error as e:
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