#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
    echo "Uso: $0 URL_DEL_REPOSITORIO"
    exit 1
fi

repository_url="$1"
project_dir="TEIS-DjangoSOLID"

git clone "$repository_url" "$project_dir"
cd "$project_dir"
docker compose up -d --build
docker ps
