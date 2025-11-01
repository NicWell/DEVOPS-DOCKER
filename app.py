import os
from flask import Flask, request, jsonify
from db import db
from models import Livro

def create_app():
    app = Flask(__name__)

    # Lê URL do DB a partir da variável de ambiente DATABASE_URL
    # Ex: postgresql://biblioteca_user:senha@db:5432/biblioteca_db
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/livros', methods=['GET'])
    def listar_livros():
        livros = Livro.query.all()
        return jsonify([l.to_dict() for l in livros])

    @app.route('/livros/<int:id>', methods=['GET'])
    def obter_livro(id):
        livro = Livro.query.get_or_404(id)
        return jsonify(livro.to_dict())

    @app.route('/livros', methods=['POST'])
    def adicionar_livro():
        dados = request.json or {}
        novo_livro = Livro(
            titulo=dados.get('titulo'),
            autor=dados.get('autor'),
            ano_publicacao=dados.get('ano_publicacao'),
            genero=dados.get('genero')
        )
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify(novo_livro.to_dict()), 201

    @app.route('/livros/<int:id>', methods=['PUT'])
    def atualizar_livro(id):
        livro = Livro.query.get_or_404(id)
        dados = request.json or {}
        livro.titulo = dados.get('titulo', livro.titulo)
        livro.autor = dados.get('autor', livro.autor)
        livro.ano_publicacao = dados.get('ano_publicacao', livro.ano_publicacao)
        livro.genero = dados.get('genero', livro.genero)
        db.session.commit()
        return jsonify(livro.to_dict())

    @app.route('/livros/<int:id>', methods=['DELETE'])
    def deletar_livro(id):
        livro = Livro.query.get_or_404(id)
        db.session.delete(livro)
        db.session.commit()
        return jsonify({'mensagem': 'Livro removido com sucesso!'})

    return app

if __name__ == '__main__':
    app = create_app()
    # em produção o Gunicorn no Docker rodará, mas para debug local:
    app.run(host='0.0.0.0', port=5000)
