[![CI/CD Pipeline](https://github.com/NicWell/DEVOPS-DOCKER/actions/workflows/cicd.yml/badge.svg)](https://github.com/NicWell/DEVOPS-DOCKER/actions/workflows/cicd.yml)

# CI/CD e Deploy
## Pipeline CI/CD
 O projeto conta com automação via GitHub Actions que realiza:
  1. Instalação de dependências e execução de Testes Unitários (Pytest).
  2. Build da imagem Docker.
  3. Push da imagem para o Docker Hub (nicwell/biblioteca-api).
  3. Variáveis de Ambiente (Secrets)
## Para o pipeline funcionar, as seguintes Secrets foram configuradas no GitHub:
  1. DOCKER_USERNAME: Usuário do Docker Hub.
  2. DOCKER_PASSWORD: Senha/Token do Docker Hub.
  3. (HOST, USERNAME e KEY estão preparados para o deploy via SSH).


# DEVOPS-DOCKER
ATIVIDADE SUBMETIDA A DISCIPLINA DE DEVOPS

# Biblioteca API

Bem-vindo à **API da Biblioteca!**  
Este projeto fornece uma **API RESTful** simples para gerenciar uma coleção de livros, construída com **Flask** e **PostgreSQL**, e totalmente **containerizada com Docker**.

---

## Funcionalidades

- Listar todos os livros  
- Obter um livro específico por ID  
- Adicionar um novo livro  
- Atualizar os detalhes de um livro existente  
- Remover um livro  

---

## Arquitetura e Tecnologias

| Componente        | Tecnologia          |
|-------------------|--------------------|
| **Backend**       | Flask              |
| **Banco de Dados**| PostgreSQL         |
| **Servidor WSGI** | Gunicorn           |
| **Containerização** | Docker + Docker Compose |

O projeto utiliza um **Dockerfile multi-stage** para criar uma **imagem de produção otimizada**, pequena e segura.  
O **Docker Compose** orquestra os contêineres da aplicação e do banco de dados, gerenciando rede, volumes e variáveis de ambiente.

---

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados na sua máquina:

-  **Docker**: [Instruções de Instalação](https://docs.docker.com/get-docker/)
-  **Docker Compose**: geralmente já vem incluso no Docker Desktop. Caso precise instalar separadamente, siga [estas instruções](https://docs.docker.com/compose/install/).

---

## Configuração do Ambiente

O projeto utiliza **variáveis de ambiente** para configurar a conexão com o banco de dados.  
Siga os passos abaixo para preparar o ambiente:

### 1 Clone o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2 Crie o Arquivo de Variáveis de Ambiente

Existe um arquivo de exemplo chamado `.env.example`.  
Crie uma cópia dele chamada `.env`:

```bash
cp .env.example .env
```

### 3 Revise o Arquivo `.env` (Opcional)

As credenciais padrão foram configuradas para funcionar localmente.  
Você pode personalizá-las conforme desejar:

```dotenv
# .env

# Configurações do superusuário do PostgreSQL (usado para inicialização)
POSTGRES_SUPERUSER=postgres
POSTGRES_SUPERPASS=postgres123

# Configurações do banco de dados e do usuário da aplicação
POSTGRES_DB=bibliotecadb
APP_DB_USER=biblioteca_user
APP_DB_PASSWORD=secret
```

---

## Como Executar a Aplicação

Com o Docker e o Docker Compose instalados e o arquivo `.env` configurado, executar o projeto é muito simples.

### 1 Construa as Imagens e Inicie os Contêineres

No diretório raiz do projeto (onde está o `docker-compose.yml`), execute:

```bash
docker-compose up --build
```

O comando `docker-compose up`:
- Baixará a imagem do PostgreSQL;
- Construirá a imagem da aplicação Flask;
- Criará as redes e volumes necessários;
- Iniciará os contêineres.

A flag `--build` força a reconstrução da imagem da aplicação, garantindo que alterações recentes no código ou dependências sejam aplicadas.

Durante a primeira execução, o banco será inicializado, as tabelas criadas e a aplicação iniciará.  
Você verá os logs dos serviços `app` e `db` no terminal.

---

### 2 Verifique se os Contêineres estão Rodando

Em um novo terminal, execute:

```bash
docker-compose ps
```

Você deverá ver dois contêineres (app e db) com status **Up** ou **running**.

---

## 🔗 Usando a API

A aplicação estará disponível em:  
**http://localhost:5000**

Você pode usar ferramentas como **Postman**, **Insomnia** ou **curl** para interagir com os endpoints.

---

### Exemplo com `curl`

#### ➕ Adicionar um novo livro

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "titulo": "O Senhor dos Anéis",
  "autor": "J.R.R. Tolkien",
  "ano_publicacao": 1954,
  "genero": "Fantasia"
}' http://localhost:5000/livros
```

#### Listar todos os livros

```bash
curl http://localhost:5000/livros
```

---

**Dica:** Para testar e explorar a API, é recomendável usar o **Insomnia** ou **Postman**, facilitando o envio e a visualização de requisições HTTP.

---

## Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se à vontade para usar, modificar e contribuir!

---

**Autor:** Wellington Nicacio 
**Repositório:** [https://github.com/NicWell/DEVOPS-DOCKER](https://github.com/NicWell/DEVOPS-DOCKER)

