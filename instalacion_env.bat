@echo off
echo 1. Creando el entorno virtual 'entTiendaRopa'...
py -m venv entTiendaRopa

echo 2. Activando el entorno e instalando dependencias...
call entTiendaRopa\Scripts\activate.bat
pip install -r requirements.txt

echo 3. Aplicando migraciones a la base de datos...
py manage.py migrate

echo Listo.
cmd /k