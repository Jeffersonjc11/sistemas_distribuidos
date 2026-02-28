# Proyecto de Sistemas Distribuidos (Python + Docker)

Plantilla de microservicios con API Gateway y base de datos preparada para separacion por dominio.

## Arquitectura actual

- `gateway`: punto unico de entrada para clientes.
- `identity-service`: microservicio interno (dominio: identidad/vehiculos).
- `service-b`: microservicio interno (dominio sugerido: operaciones de parqueo).
- `service-c`: microservicio interno (dominio sugerido: cobro/facturacion).
- `postgres`: una sola instancia de PostgreSQL para todo el sistema.

```text
Cliente -> gateway:8000
              |
              +-> identity-service:8001
              +-> service-b:8002
              +-> service-c:8003

identity-service --\
service-b -----+--> postgres:5432 (misma instancia)
service-c ----/
```

## Estrategia de base de datos

Se usa **1 contenedor PostgreSQL** con **1 base por microservicio**:

- `db_identity` (usuario: `identity_user`)
- `db_parking_ops` (usuario: `ops_user`)
- `db_billing` (usuario: `billing_user`)

Inicializacion automatica:

- Script: `db/init/01-init.sql`
- Se ejecuta automaticamente al primer arranque de `postgres` (cuando el volumen esta vacio).

Conexion por servicio (ya preparado en `docker-compose.yml`):

- `identity-service`: `DATABASE_URL=postgresql://identity_user:identity_pass@postgres:5432/db_identity`
- `service-b`: `DATABASE_URL=postgresql://ops_user:ops_pass@postgres:5432/db_parking_ops`
- `service-c`: `DATABASE_URL=postgresql://billing_user:billing_pass@postgres:5432/db_billing`

Regla de diseno:

- Cada microservicio consulta solo su propia BD.
- Para leer datos de otro dominio, usar API entre servicios, no SQL cruzado.

## Endpoints del gateway

- `GET /`
- `GET /health`
- `GET /api/identity`
- `GET /api/service-a`
- `GET /api/service-b`
- `GET /api/service-c`

## Estructura

```text
.
|- docker-compose.yml
|- db/
|  `- init/
|     `- 01-init.sql
|- gateway/
|- service-a/
|- service-b/
`- service-c/
```

## Comandos (cuando decidas ejecutarlo)

Levantar:

```bash
docker compose up -d --build
```

Ver logs:

```bash
docker compose logs -f postgres
docker compose logs -f gateway
```

Detener:

```bash
docker compose down
```

