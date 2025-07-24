@echo off
cd /d "%~dp0"
echo.
echo ================================================
echo     SISTEMA SISGES-PF - SYNC Y EJECUCIÓN
echo ================================================
echo.

:: Crear entorno virtual si no existe
if not exist "venv\Scripts\activate.bat" (
    echo 🔧 Entorno virtual no encontrado. Creando entorno virtual...
    python -m venv venv
)

:: Activar entorno virtual
echo ✅ Activando entorno virtual...
call venv\Scripts\activate.bat

:: Instalar dependencias
echo 🧩 Instalando dependencias...
pip install -r requirements.txt

:: Sincronizar cambios desde GitHub
echo 🔄 Sincronizando con GitHub (pull)...
git pull

:: Agregar cambios locales automáticamente
git add .

:: Commit automático
set msg=Sincronización automática y ejecución
git commit -m "%msg%" >nul 2>&1

:: Subir a GitHub
echo 🚀 Subiendo cambios a GitHub...
git push >nul 2>&1

:: Lanzar la aplicación
echo 🚀 Ejecutando sistema SISGES-PF...
streamlit run app\reporteria_full.py

pause