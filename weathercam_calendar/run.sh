#!/usr/bin/with-contenv bashio
set -euo pipefail

export ROOT_DIR="$(bashio::config 'root_dir')"
export APP_TITLE="$(bashio::config 'title')"

echo "Starte Weathercam Calendar"
echo "ROOT_DIR=${ROOT_DIR}"
echo "APP_TITLE=${APP_TITLE}"

exec python3 /app.py
