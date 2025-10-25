from flask import Flask, jsonify, request
from config import Config
from db import db
from models import Livro

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Cria as tabelas no banco se ainda não existirem
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"mensagem": "API da Biblioteca esta rodando!"})

# criação de um novo livro
@app.route('/livros', methods=['POST'])
def criar_livro():
    dados = request.get_json()
    novo = Livro(
        titulo=dados.get('titulo'),
        autor=dados.get('autor'),
        ano_publicacao=dados.get('ano_publicacao'),
        genero=dados.get('genero')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Livro criado com sucesso!", "livro": novo.to_dict()}), 201

# listagem dos livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()
    return jsonify([l.to_dict() for l in livros])

# listagem de livros por id
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.to_dict())

#update da rota livros
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    livro = Livro.query.get_or_404(id)
    dados = request.get_json()
    livro.titulo = dados.get('titulo', livro.titulo)
    livro.autor = dados.get('autor', livro.autor)
    livro.ano_publicacao = dados.get('ano_publicacao', livro.ano_publicacao)
    livro.genero = dados.get('genero', livro.genero)
    db.session.commit()
    return jsonify({"mensagem": "Livro atualizado com sucesso!", "livro": livro.to_dict()})

# delete da rota livros
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({"mensagem": "Livro deletado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
