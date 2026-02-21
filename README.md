# Proyecto de Sistemas Distribuidos (Python + Docker)

Plantilla base de microservicios para la materia de sistemas distribuidos.
El proyecto implementa un patron de **API Gateway**:

- `gateway`: punto unico de entrada para clientes.
- `service-a`: microservicio interno.
- `service-b`: microservicio interno.

Cada servicio tiene su propio `Dockerfile`, su propio `requirements.txt` y se despliega como contenedor independiente.

## Arquitectura

```text
Cliente (host)
     |
     | HTTP :8000
     v
 gateway (FastAPI)
   |            |
   |            |
   v            v
service-a     service-b
(FastAPI)     (FastAPI)
:8001         :8002
```

Reglas de red:

- Solo `gateway` publica puerto al host: `8000:8000`.
- `service-a` y `service-b` usan `expose`, por lo tanto solo son accesibles desde la red interna de Docker.
- Los nombres de servicio de Compose (`service-a`, `service-b`) funcionan como DNS interno para que el gateway los consuma.

## Como funciona el flujo

1. El cliente llama a `http://localhost:8000/...`.
2. El `gateway` recibe la solicitud.
3. Si es una ruta de proxy, el gateway llama por HTTP interno al microservicio correspondiente.
4. El microservicio responde JSON.
5. El gateway retorna la respuesta al cliente.

Ejemplo:

1. Cliente -> `GET /api/service-a`
2. Gateway -> `GET http://service-a:8001/data`
3. Service A -> JSON de usuarios
4. Gateway -> devuelve ese JSON al cliente

Si falla la llamada interna (timeout, conexion o error HTTP), el gateway responde `502`.

## Endpoints

Gateway (`localhost:8000`):

- `GET /`: mensaje base y rutas disponibles.
- `GET /health`: salud del gateway y chequeo agregado de `service-a` y `service-b`.
- `GET /api/service-a`: proxy hacia `service-a:/data`.
- `GET /api/service-b`: proxy hacia `service-b:/data`.

Service A (interno):

- `GET /health`
- `GET /data` (datos de ejemplo del dominio "usuarios")

Service B (interno):

- `GET /health`
- `GET /data` (datos de ejemplo del dominio "ordenes")

## Variables de entorno

Definidas en `docker-compose.yml`:

- `gateway`: `PORT=8000`, `SERVICE_A_URL=http://service-a:8001`, `SERVICE_B_URL=http://service-b:8002`
- `service-a`: `PORT=8001`
- `service-b`: `PORT=8002`

## Estructura del proyecto

```text
.
|- docker-compose.yml
|- .dockerignore
|- README.md
|- gateway/
|  |- Dockerfile
|  |- requirements.txt
|  `- app/
|     |- __init__.py
|     `- main.py
|- service-a/
|  |- Dockerfile
|  |- requirements.txt
|  `- app/
|     |- __init__.py
|     `- main.py
`- service-b/
   |- Dockerfile
   |- requirements.txt
   `- app/
      |- __init__.py
      `- main.py
```

## Ejecutar

Construir y levantar:

```bash
docker compose up -d --build
```

Probar por gateway:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/service-a
curl http://localhost:8000/api/service-b
```

Ver logs:

```bash
docker compose logs -f gateway
docker compose logs -f service-a
docker compose logs -f service-b
```

Detener:

```bash
docker compose down
```

## Como extender con un nuevo servicio

Para agregar, por ejemplo, `service-c`:

1. Crear carpeta `service-c/` con `Dockerfile`, `requirements.txt` y `app/main.py`.
2. Agregar `service-c` a `docker-compose.yml` con su `PORT` y `expose`.
3. Definir en gateway la URL del servicio (por variable de entorno).
4. Crear endpoint en el gateway para proxy a `service-c`.
5. Reconstruir: `docker compose up -d --build`.

Con este patron, el cliente nunca se conecta directo a microservicios internos: siempre entra por el gateway.

