# FastApi-by-everchicasp

### Levantar aplicación usando nginx
```
apt install nginx
apt install nodejs
apt install npm
npm install pm2@latest -g
```

### Comandos pm2 
ver procesos 
```
pm2 list
```

### Crear entorno virtual
```
python3 -m venv info-projects
source venv/bin/activate
pip install -r requirements.txt
```

### Levantar proyecto con pm2
```
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name my-info-projects-api
```

### Docker
```
```
