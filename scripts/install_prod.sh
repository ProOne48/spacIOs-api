#!/usr/bin/env bash

set -Eeuo pipefail

PYTHON_VERSION="${PYTHON_VERSION:-3.14}"
VENV_DIR="${VENV_DIR:-venv}"

echo_installing()
{
    echo "########################################################################"
    echo " Installing $1"
    echo "########################################################################"
}

if ! command -v uv >/dev/null 2>&1; then
    echo_installing "uv"

    curl -LsSf https://astral.sh/uv/install.sh | sh

    export PATH="${HOME}/.local/bin:${PATH}"
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "ERROR: uv no está disponible después de instalarlo."
    echo "Prueba a abrir una terminal nueva o ejecuta:"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
    exit 1
fi

echo_installing "Python ${PYTHON_VERSION}"

uv python install "${PYTHON_VERSION}"

echo_installing "virtual environment"

uv venv \
    --clear \
    --python "${PYTHON_VERSION}" \
    "${VENV_DIR}"

echo_installing "Python dependencies"

uv pip install \
    --python "${VENV_DIR}/bin/python" \
    --upgrade \
    pip

uv pip install \
    --python "${VENV_DIR}/bin/python" \
    --requirement requirements.txt

uv pip install \
    --python "${VENV_DIR}/bin/python" \
    flake8

"${VENV_DIR}/bin/python" -m pip check

echo "########################################################################"
echo " Environment ready"
echo " Python: $("${VENV_DIR}/bin/python" --version)"
echo " Executable: ${VENV_DIR}/bin/python"
echo "########################################################################"
echo "Activate with:"
echo "source ${VENV_DIR}/bin/activate"