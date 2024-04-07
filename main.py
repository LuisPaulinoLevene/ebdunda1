import sqlite3
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Função para criar todas as tabelas necessárias
# Função para criar a tabela 'usuarioss', se ela não existir
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

        # Redirecionar para a página de sucesso (pode ser a mesma página de registro)
        return RedirectResponse(url="/registro")

    except Exception as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao registrar usuário:", e)
        # Retornar uma mensagem de erro ao cliente
        raise HTTPException(status_code=500, detail="Erro ao registrar usuário. Por favor, tente novamente.")
    if user:
        return "usuarioss"

    # Verificar se as credenciais estão na tabela acessoprof
    conn = sqlite3.connect("Maquina.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM acessoprof WHERE username = ? AND password = ?", (username, password))
    professor_user = cursor.fetchone()
    conn.close()


    # Se as credenciais não corresponderem a nenhuma tabela
    return "invalid"

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

        return True

    except sqlite3.Error as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao excluir o usuário:", e)
        return False


# Função para exibir os usuários em uma tabela HTML
def generate_users_table(usuarios):
    table_content = "<h2>Usuários</h2>"
    table_content += "<table border='1'><tr><th>ID</th><th>Username</th><th>Password</th><th>Ação</th></tr>"
    for usuario in usuarios:
        table_content += f"<tr><td>{usuario[0]}</td><td>{usuario[1]}</td><td>{usuario[2]}</td>"
        table_content += f"<td><form method='post' action='/apagar_usuario/{usuario[0]}'><button type='submit'>Apagar</button></form></td></tr>"
    table_content += "</table>"
    return table_content

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
        table_content = generate_users_table(usuarios)

        # Retornar a resposta HTML
        return HTMLResponse(content=table_content)

    except sqlite3.Error as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao buscar os usuários:", e)
        # Levantar uma exceção HTTP 500
        raise HTTPException(status_code=500, detail="Erro ao buscar os usuários. Por favor, tente novamente.")

# Função para excluir um usuário do banco de dados
def delete_user(user_id: int):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect("Maquina.db")
        cursor = conn.cursor()

        # Excluir o usuário da tabela pelo ID
        cursor.execute("DELETE FROM usuarioss WHERE id = ?", (user_id,))
        conn.commit()

        # Reorganizar os IDs na tabela após a exclusão
        cursor.execute("UPDATE usuarioss SET id = id - 1 WHERE id > ?", (user_id,))
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

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

# Usar a função validate_credentials() na função login()
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_type = validate_credentials(username, password)

    if user_type == "usuarioss":
        # Credenciais válidas na tabela usuarios, redireciona para a página menu2.html
        return RedirectResponse("/menu2")

    else:
        # Credenciais inválidas, exibe a mensagem na página menu.html
        return templates.TemplateResponse("index.html", {"request": request, "mensagem": "Credenciais inválidas"})

    # Função para registrar o usuário "maquina" na tabela 'admin'



# Rota para a página utilizadores.html
@app.get("/utilizadores.html")
async def show_utilizadores(request: Request):
    return FileResponse("utilizadores.html")

# Rota para a página inicial
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request, mensagem: str = None):
    return FileResponse("index.html")

# Rota para processar o formulário de registro de usuário

@app.get("/registrar_usuario", response_class=HTMLResponse)
async def show_registrar_usuario(request: Request):
    return FileResponse("utilizadores.html")
@app.post("/registrar_usuario")
async def registrar_usuario(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect("Maquina.db")
        cursor = conn.cursor()

        # Inserir os dados do usuário na tabela 'usuarioss'
        cursor.execute(
            "INSERT INTO usuarioss (username, password) VALUES (?, ?)",
            (username, password)
        )

        # Commit a transação
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        # Retornar uma mensagem de sucesso
        return {"message": "Usuário registrado com sucesso!"}

    except sqlite3.Error as e:
        # Em caso de erro, imprimir uma mensagem de erro
        print("Erro ao registrar usuário:", e)
        # Retornar uma mensagem de erro ao cliente
        return {"error": "Erro ao registrar usuário. Por favor, tente novamente."}


# Rota para exibir a tabela de usuários
@app.get("/lista_usuarios", response_class=HTMLResponse)
async def show_usuarios(request: Request):
    conn = sqlite3.connect("Maquina.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarioss")
    usuarios = cursor.fetchall()
    conn.close()
    return FileResponse("usuarios.html", {"request": request, "usuarioss": usuarios})


# Função para obter todos os usuários
def get_all_users():
    conn = sqlite3.connect("Maquina.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarioss")
    users = cursor.fetchall()
    conn.close()
    return users

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)