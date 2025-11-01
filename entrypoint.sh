#!/bin/sh
# entrypoint.sh — inicialização do app Flask no Gunicorn

echo "Iniciando a aplicação Flask via Gunicorn..."

# O docker-compose com 'depends_on' e 'healthcheck' já garantiu que o DB está pronto.
# O loop 'while' foi removido por ser desnecessário.

echo "Iniciando aplicação..."

# Executa o Gunicorn
exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"