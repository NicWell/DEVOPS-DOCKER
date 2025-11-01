# ==============================
# Stage 1 — Builder (instala dependências)
# ==============================
FROM python:3.11-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema (para compilar psycopg2 e libs)
RUN apk add --no-cache build-base libffi-dev postgresql-dev

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ==============================
# Stage 2 — Runtime (produção)
# ==============================
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala apenas o essencial
RUN apk add --no-cache libpq curl bash

# Cria usuário não-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copia código-fonte e dependências do builder
COPY --from=builder /usr/local /usr/local
COPY . .

# Converte quebra de linha Windows → Linux e dá permissão de execução
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

USER appuser

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
