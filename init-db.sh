#!/bin/bash
set -e

# Este script é executado dentro do container postgres na primeira inicialização.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Cria o usuário da aplicação se ele não existir
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${APP_DB_USER}') THEN
            CREATE ROLE ${APP_DB_USER} LOGIN PASSWORD '${APP_DB_PASSWORD}';
        END IF;
    END
    \$\$;

    -- Concede permissão para o usuário se conectar ao banco de dados
    GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${APP_DB_USER};

    -- ## AQUI ESTÁ A CORREÇÃO PRINCIPAL ##
    -- Concede permissão para USAR e CRIAR no schema 'public'
    GRANT USAGE, CREATE ON SCHEMA public TO ${APP_DB_USER};

    -- [OPCIONAL, MAS RECOMENDADO PARA EVITAR FUTUROS PROBLEMAS]
    -- Altera os privilégios padrão. Qualquer tabela ou sequência que seja
    -- criada no futuro neste schema por qualquer usuário (incluindo o superusuário)
    -- automaticamente dará todos os privilégios ao APP_DB_USER.
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${APP_DB_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${APP_DB_USER};
EOSQL