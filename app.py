from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

users = {}

# Página cadastro (HTML simples, só para abrir no navegador)
@app.route('/cadastro')
def cadastro():
    return render_template_string('''
    <h2>Cadastro</h2>
    <form id="formCadastro" onsubmit="submitCadastro(event)">
        <input id="nome" placeholder="Nome" required><br>
        <input id="email" placeholder="Email" type="email" required><br>
        <input id="senha" placeholder="Senha" type="password" required><br>
        <button type="submit">Cadastrar</button>
    </form>
    <div id="mensagem"></div>
    <script>
    async function submitCadastro(e) {
        e.preventDefault();
        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        const res = await fetch('/api/cadastro', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({nome, email, senha})
        });
        const data = await res.json();
        document.getElementById('mensagem').innerText = data.message;
    }
    </script>
    ''')

# API cadastro
@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    data = request.json
    email = data.get('email')
    if email in users:
        return jsonify(message='Email já cadastrado'), 400
    users[email] = {'nome': data.get('nome'), 'senha': data.get('senha')}
    return jsonify(message='Cadastro com sucesso')

# Página login
@app.route('/login')
def login():
    return render_template_string('''
    <h2>Login</h2>
    <form id="formLogin" onsubmit="submitLogin(event)">
        <input id="emailLogin" placeholder="Email" type="email" required><br>
        <input id="senhaLogin" placeholder="Senha" type="password" required><br>
        <button type="submit">Entrar</button>
    </form>
    <div id="mensagemLogin"></div>
    <script>
    async function submitLogin(e) {
        e.preventDefault();
        const email = document.getElementById('emailLogin').value;
        const senha = document.getElementById('senhaLogin').value;
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, senha})
        });
        const data = await res.json();
        document.getElementById('mensagemLogin').innerText = data.message;
    }
    </script>
    ''')

# API login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    user = users.get(email)
    if not user or user['senha'] != senha:
        return jsonify(message='Credenciais inválidas'), 401
    return jsonify(message='Login bem-sucedido')

if __name__ == '__main__':
    app.run(debug=True)
