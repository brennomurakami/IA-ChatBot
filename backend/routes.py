from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, login_required, logout_user, current_user
from backend.db import mysql
from backend.gpt import client
from backend.user import User
from backend.funcoes import *
login_routes = Blueprint('login_routes', __name__)
index_routes = Blueprint('index_routes', __name__)
cadastrar_routes = Blueprint('cadastrar_routes', __name__)

thread = ''
# Rota para fazer login
@login_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Consulta ao banco de dados para verificar se o usuário e a senha estão corretos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        user = User(user_id=user_data[0], username=user_data[1])
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso!'})
    else:
        return jsonify({'error': 'Nome de usuário ou senha incorretos!'}), 401
    
# Rota para cadastrar um usuário
@cadastrar_routes.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Consulta ao banco de dados para verificar se o usuário já existe
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        return jsonify({'error': 'Nome de usuário já existe!'}), 400

    # Insere o novo usuário no banco de dados
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'})


# Rota do cadastro
@cadastrar_routes.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota Inicial
@index_routes.route('/')
def index():
    return render_template('login.html')

# Rota para fazer logout
@index_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

# Rota da home
@index_routes.route('/home')
@login_required
def home():
    username = current_user.username  # Aqui, current_user é uma variável fornecida pelo Flask-Login
    user_chats = User.get_user_chats()
    return render_template('index.html', username=username, user_chats=user_chats)

# Criando rota para mandar a mensagem e receber a resposta
@index_routes.route('/get_response/<int:chat_id>', methods=['POST'])
@login_required
def get_response(chat_id):
    global thread
    data = request.get_json()
    user_message = data.get('message')
    mensagem_usuario = user_message
    resposta = "FUNCOES NECESSARIAS121"
    while "FUNCOES NECESSARIAS121" in resposta or "SQL121" in resposta:
        message = client.beta.threads.messages.create(
        thread_id=thread,
        role="user",
        content=user_message
        )

        run = client.beta.threads.runs.create_and_poll(
        thread_id=thread,
        assistant_id="asst_8dZmPoQiKTMkaxUjMuS6uUuc",
        max_completion_tokens=4000 # +/- 2000 palavras com 5 caracteres cada, para entrada e saida de dados
        )
        messages = client.beta.threads.messages.list(thread_id=thread)
        resposta =  messages.data[0].content[0].text.value
        print(resposta)
        if "FUNCOES NECESSARIAS121:" in resposta.upper() and "SQL121" in resposta.upper():
            user_message = processar_mensagem(resposta)
        elif "FUNCOES NECESSARIAS121:" in resposta.upper():
            user_message = processar_funcoes(resposta)
        elif "SQL121:" in resposta.upper():
            user_message = processar_sql(resposta)
    # Salvando a mensagem do usuário e a resposta do servidor no banco de dados
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (text_usuario, text_servidor, chat_id) VALUES (%s, %s, %s)", (mensagem_usuario, messages.data[0].content[0].text.value, chat_id))
    mysql.connection.commit()
    cur.close()
    print("\n\n",messages.data[0].content[0].text.value)
    # Retorna a resposta ao usuário
    return jsonify({'message': messages.data[0].content[0].text.value})

@index_routes.route('/add_chat', methods=['POST'])
def add_chat():
    data = request.get_json()
    title = data.get('title')
    user_id = current_user.id
    global thread
    thread = client.beta.threads.create()
    thread = thread.id
    # Insere um novo chat no banco de dados
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO chats (title, user_id, id_gpt) VALUES (%s, %s, %s)", (title, user_id, thread))
    mysql.connection.commit()
    
    # Recupera o ID do chat recém-adicionado
    chat_id = cur.lastrowid
    
    cur.close()

    # Retorna os dados do chat recém-adicionado
    return jsonify({'chat_id': chat_id, 'title': title})

@index_routes.route('/get_messages/<int:chat_id>')
@login_required
def get_messages(chat_id):
    # Consulte o banco de dados para obter as mensagens correspondentes ao chat_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages WHERE chat_id = %s", (chat_id,))
    messages = cur.fetchall()
    cur.close()
    # Formate as mensagens como uma lista de dicionários para facilitar a serialização em JSON
    formatted_messages = [{"id": message[0], "usuario": message[1], "servidor": message[2]} for message in messages]
    global thread
    # Consulte o banco de dados para obter as mensagens correspondentes ao chat_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_gpt FROM chats WHERE id = %s", (chat_id,))
    messages = cur.fetchone()
    cur.close()
    thread = messages[0]
    thread = thread.strip("'")
    # Retorne as mensagens como resposta JSON
    return jsonify(formatted_messages)

@index_routes.route('/delete_chat/<int:chat_id>', methods=['POST'])
@login_required
def delete_chat(chat_id):
    try:
        # Deleta todas as mensagens associadas ao chat_id
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM messages WHERE chat_id = %s", (chat_id,))
        mysql.connection.commit()

        # Deleta o chat_id
        cur.execute("DELETE FROM chats WHERE id = %s", (chat_id,))
        mysql.connection.commit()

        cur.close()

        return jsonify({"message": "Chat deletado com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@index_routes.route('/update_chat_title/<int:chat_id>', methods=['POST'])
@login_required
def update_chat_title(chat_id):
    try:
        data = request.get_json()
        new_title = data.get('title')

        cur = mysql.connection.cursor()
        cur.execute("UPDATE chats SET title = %s WHERE id = %s", (new_title, chat_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Título do chat atualizado com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500