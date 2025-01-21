# FastApi-by-everchicasp

### Crear entorno virtual Windows
```
python3 -m venv info-projects
source venv/Scripts/activate
pip install -r requirements.txt
```

### Pasos para desplegar FastAPI en IIS
#### 1. Instalar dependencias necesarias
Antes de continuar, asegúrate de tener instalado lo siguiente en tu servidor Windows:

- Python (versión 3.8 o superior). Descárgalo de python.org
- IIS (Internet Information Services)
- WSGI Server para IIS, utilizaremos wfastcgi
- Para instalar Python, descarga el instalador de python.org y asegúrate de marcar la casilla "Add Python to PATH".

#### 2. Instalar FastAPI y dependencias necesarias
Abre PowerShell y ejecuta:

```pip install fastapi uvicorn wfastcgi```

Esto instalará:
FastAPI: Framework web.
Uvicorn: Servidor ASGI necesario para ejecutar FastAPI.
wfastcgi: Módulo que permite a IIS ejecutar aplicaciones Python con FastCGI.

#### 3. Configurar IIS para soportar FastCGI
Abre "Administrador de IIS" (IIS Manager).

Selecciona el servidor en el panel izquierdo.

Haz doble clic en "FastCGI Settings".

Agrega una nueva aplicación con los siguientes valores:

Full Path: Ruta completa de python.exe (ejemplo: C:\Python312\python.exe).
Arguments: C:\Python312\Scripts\wfastcgi-enable (ajusta la ruta según la instalación de Python).
Environment Variables:
Agrega una variable con la clave PYTHONPATH y el valor apuntando a la carpeta de tu aplicación FastAPI.
Guarda los cambios.

#### 4. Crear archivo de configuración web.config
En la raíz de tu aplicación FastAPI, crea un archivo llamado web.config con el siguiente contenido:

```
<configuration>
  <system.webServer>
    <handlers>
      <add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" scriptProcessor="C:\Python312\python.exe|C:\Python312\Scripts\wfastcgi-enable" resourceType="Unspecified" requireAccess="Script"/>
    </handlers>
    <fastCgi>
      <application fullPath="C:\Python312\python.exe" arguments="C:\Python312\Scripts\wfastcgi-enable" instanceMaxRequests="10000">
        <environmentVariables>
          <environmentVariable name="PYTHONPATH" value="C:\inetpub\wwwroot\example-fastapi" />
          <environmentVariable name="WSGI_HANDLER" value="app.main:app" />
          <environmentVariable name="UVICORN_CMD" value="uvicorn" />
          <environmentVariable name="PORT" value="8000" />
        </environmentVariables>
      </application>
    </fastCgi>
  </system.webServer>
</configuration>
```
Reemplaza las rutas según la ubicación de tu instalación de Python y tu proyecto.
La variable WSGI_HANDLER debe apuntar al módulo de FastAPI, por ejemplo, app.main:app.

#### 5. Configurar IIS para servir la API
Abre el Administrador de IIS.
Crea un nuevo sitio web o selecciona el sitio existente (por ejemplo, Default Web Site).
Establece la carpeta raíz en la ubicación de tu aplicación FastAPI (por ejemplo, C:\inetpub\wwwroot\example-fastapi).
Asegúrate de que la aplicación está configurada para ejecutarse con permisos adecuados (por ejemplo, permisos de lectura y ejecución).
Prueba la aplicación accediendo a http://localhost/ o a través de la IP del servidor.

#### 6. Crear un script para iniciar FastAPI
Dentro de tu aplicación FastAPI, crea un archivo run.py para ejecutar Uvicorn:

```
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")
```

#### 7. Crear un archivo .bat para iniciar la aplicación automáticamente
Puedes crear un archivo .bat para ejecutar la aplicación automáticamente al iniciar el servidor. Crea un archivo llamado start_server.bat:

```
cd C:\inetpub\wwwroot\example-fastapi
python run.py
```

Agrega este script al Inicio de Windows para ejecutarse automáticamente.

#### 8. Verificar la API FastAPI en IIS
Una vez configurado todo, accede a tu servidor a través del navegador:

Swagger UI: http://localhost/docs
Redoc: http://localhost/redoc
Si estás accediendo desde otra máquina de la red local, usa la dirección IP del servidor:
```
http://<IP-DEL-SERVIDOR>/docs
```
#### 9. Solución de problemas
Si experimentas problemas, verifica lo siguiente:

Revisa los registros de IIS en: C:\inetpub\logs\LogFiles
Asegúrate de que Python está correctamente instalado y agregado al PATH.
Verifica permisos adecuados para IIS para acceder a los archivos de la aplicación.
Asegúrate de que FastCGI está habilitado en IIS.

#### 10. Alternativa: Usar Windows Services para iniciar FastAPI
En lugar de usar IIS, también puedes configurar la aplicación como un servicio de Windows para ejecutarla automáticamente:

Instala el paquete nssm (Non-Sucking Service Manager) en Windows.
Configura el servicio con el siguiente comando en PowerShell:

```nssm install FastAPIService "C:\Python312\python.exe" "C:\inetpub\wwwroot\example-fastapi\run.py"```

Inicia el servicio:
```nssm start FastAPIService```