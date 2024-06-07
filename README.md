# FastApi-by-everchicasp

### Levantar aplicación usando nginx
```
```
apt install nginx
apt install nodejs
apt install npm
npm install pm2@latest -g
```
```

### Comandos pm2 
ver procesos 
```
pm2 list
```
```
pm2 list
```

### Crear entorno virtual
```
```
python3 -m venv info-projects
source venv/bin/activate
pip install -r requirements.txt
```
```

### Levantar proyecto con pm2
```
```
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name my-info-projects-api
```

### Docker

```
docker build -f Dockerfile.dev -t info-projects-dev .
docker build -t info-projects-prod .

docker run --name info-dev -p 8000:8000  -v $(pwd):/app info-projects-dev
```
