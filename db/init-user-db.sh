#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER lupi;
    CREATE DATABASE lupi;
    GRANT ALL PRIVILEGES ON DATABASE lupi TO lupi;
EOSQL
