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

# Obtener el home real del usuario, evitando las modificaciones de Snap.
USER_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
UV_BIN_DIR="${USER_HOME}/.local/bin"
UV_BIN="${UV_BIN_DIR}/uv"

if ! command -v uv >/dev/null 2>&1 && [[ ! -x "${UV_BIN}" ]]; then
    echo_installing "uv"

    mkdir -p "${UV_BIN_DIR}"

    curl -LsSf https://astral.sh/uv/install.sh |
        env UV_INSTALL_DIR="${UV_BIN_DIR}" sh
fi

export PATH="${UV_BIN_DIR}:${PATH}"
hash -r

if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
elif [[ -x "${UV_BIN_DIR}/uv" ]]; then
    UV_BIN="${UV_BIN_DIR}/uv"
else
    echo "ERROR: uv no está disponible después de instalarlo."
    echo "Directorio esperado: ${UV_BIN_DIR}"
    exit 1
fi

echo "Using uv: ${UV_BIN}"
"${UV_BIN}" --version

echo_installing "Python ${PYTHON_VERSION}"

"${UV_BIN}" python install "${PYTHON_VERSION}"

echo_installing "virtual environment"

"${UV_BIN}" venv \
    --clear \
    --python "${PYTHON_VERSION}" \
    "${VENV_DIR}"

echo_installing "Python dependencies"

"${UV_BIN}" pip install \
    --python "${VENV_DIR}/bin/python" \
    --upgrade \
    pip

"${UV_BIN}" pip install \
    --python "${VENV_DIR}/bin/python" \
    --requirement requirements-dev.txt

"${UV_BIN}" pip install \
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