import pytest
from app import create_app
from db import db

# --- FIXTURES (Configuração do Ambiente) ---

@pytest.fixture
def app():
    """
    Cria uma instância da aplicação configurada para testes.
    Substitui o PostgreSQL por SQLite em memória para ser rápido e isolado.
    """
    # 1. Cria a app original
    app = create_app()

    # 2. Força configurações de teste
    app.config.update({
        "TESTING": True,
        # O banco em memória garante que não afetamos o Postgres do Docker
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  
    })

    # 3. Cria as tabelas nesse banco de memória
    with app.app_context():
        db.create_all()
        yield app
        
        # 4. Limpeza após o teste rodar
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Retorna um cliente HTTP para fazermos requisições (GET, POST, etc)."""
    return app.test_client()

# --- CASOS DE TESTE ---

def test_listar_livros_vazio(client):
    """Verifica se a API retorna lista vazia quando não tem livros."""
    response = client.get('/livros')
    assert response.status_code == 200
    assert response.json == []

def test_criar_livro(client):
    """Verifica se é possível criar um livro via POST."""
    novo_livro = {
        "titulo": "Dom Quixote",
        "autor": "Miguel de Cervantes",
        "ano_publicacao": 1605,
        "genero": "Romance"
    }
    
    response = client.post('/livros', json=novo_livro)
    
    assert response.status_code == 201
    dados = response.json
    assert dados['titulo'] == "Dom Quixote"
    assert 'id' in dados  # O banco deve ter gerado um ID

def test_obter_livro(client):
    """Verifica se conseguimos buscar um livro específico pelo ID."""
    # Primeiro criamos o livro para garantir que ele existe
    client.post('/livros', json={
        "titulo": "Harry Potter", 
        "autor": "JK Rowling", 
        "ano_publicacao": 1997, 
        "genero": "Fantasia"
    })
    
    # Sabemos que será o ID 1 pois o banco é limpo a cada teste
    response = client.get('/livros/1')
    
    assert response.status_code == 200
    assert response.json['titulo'] == "Harry Potter"

def test_atualizar_livro(client):
    """Verifica o UPDATE (PUT) de um livro."""
    # 1. Cria
    client.post('/livros', json={"titulo": "Livro Velho", "autor": "X", "ano_publicacao": 2000, "genero": "Y"})
    
    # 2. Atualiza
    update_data = {"titulo": "Livro Novo"}
    response = client.put('/livros/1', json=update_data)
    
    # 3. Verifica retorno
    assert response.status_code == 200
    assert response.json['titulo'] == "Livro Novo"
    assert response.json['autor'] == "X"  # Deve manter o campo que não enviamos

def test_deletar_livro(client):
    """Verifica o DELETE."""
    # 1. Cria
    client.post('/livros', json={"titulo": "Vai Sumir", "autor": "Z", "ano_publicacao": 2020, "genero": "Z"})
    
    # 2. Deleta
    response_del = client.delete('/livros/1')
    assert response_del.status_code == 200
    
    # 3. Tenta buscar (deve dar 404 Not Found)
    response_get = client.get('/livros/1')
    assert response_get.status_code == 404