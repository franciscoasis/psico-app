#!/bin/bash
# Script para instalar dependencias y ejecutar el servidor

echo "=== Instalando dependencias ==="
pip install -r requirements.txt

echo ""
echo "=== Iniciando servidor FastAPI ==="
echo "✓ API REST disponible en http://localhost:8000"
echo "✓ Documentación en http://localhost:8000/docs"
echo "✓ WebSocket disponible en ws://localhost:8000/ws"
echo ""

python main.py
