#!/bin/bash
# Script de reparación automática para Kiosk/Web Interface
# Ejecutar en el servidor (Debian 12)

echo "🔧 Iniciando reparación de Kiosk y Dependencias..."

# 1. Definir directorios
BASE_DIR="$(pwd)"
VENV_DIR="$BASE_DIR/venv"
STATIC_JS_DIR="$BASE_DIR/web_client/static/js"

# 2. Instalar dependencias faltantes de Python
if [ -d "$VENV_DIR" ]; then
    echo "📦 Instalando librerías Python faltantes (Flask-WTF, eventlet)..."
    $VENV_DIR/bin/pip install Flask-WTF eventlet --no-cache-dir
else
    echo "❌ ERROR: No se encuentra el entorno virtual en $VENV_DIR"
    exit 1
fi

# 3. Descargar Socket.IO local
echo "🌐 Descargando socket.io.min.js local..."
mkdir -p "$STATIC_JS_DIR"
wget -q -O "$STATIC_JS_DIR/socket.io.min.js" https://cdn.socket.io/4.7.2/socket.io.min.js

# 4. Ajustar permisos de .xinitrc (por si acaso)
if [ -f ~/.xinitrc ]; then
    chmod +x ~/.xinitrc
fi

# 5. Reiniciar servicio
echo "🔄 Reiniciando servicio Neo..."
systemctl --user restart neo.service

echo "✅ Reparación completada. Verifica si la pantalla muestra la cara."
