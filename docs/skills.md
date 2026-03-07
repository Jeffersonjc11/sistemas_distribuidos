# Guia de Skills del Proyecto

Esta guia explica las skills instaladas en este repositorio, para que sirven y como pedirle a Codex que las use.

## Que es una skill

- Una skill es un paquete de instrucciones para el agente (no es una libreria de Python ni un comando de Docker).
- En este proyecto viven en `.agents/skills/`.
- Son locales al proyecto: aplican aqui, no de forma global.

## Skills instaladas

| Skill | Para que sirve | Ruta |
|---|---|---|
| `find-skills` | Buscar skills en `skills.sh` e instalar nuevas skills | `.agents/skills/find-skills` |
| `shapeup` | Guiar el proceso Shape Up de principio a fin | `.agents/skills/shapeup` |
| `distributed-systems` | Aplicar patrones de sistemas distribuidos (locks, idempotencia, resiliencia, rate limit) | `.agents/skills/distributed-systems` |
| `clean-code` | Revisar/refactorizar con principios de codigo limpio | `.agents/skills/clean-code` |
| `documentation-writer` | Escribir documentacion tecnica con enfoque Diataxis | `.agents/skills/documentation-writer` |

## Como usar una skill en la practica

La forma mas confiable es nombrarla explicitamente en tu prompt. Ejemplos:

```text
Usa la skill clean-code para revisar service-b y proponer refactor.
```

```text
Usa la skill distributed-systems para endurecer este endpoint de pagos contra reintentos duplicados.
```

Tambien puedes pedir una tarea por intencion, y Codex puede elegir la skill automaticamente:

```text
Mejora este modulo con principios de codigo limpio.
```

## Guia rapida por skill

### 1) `find-skills`

Usala cuando necesites descubrir e instalar nuevas skills.

Ejemplos de uso:

```text
Usa find-skills para buscar una skill de testing e instalarla en el proyecto.
```

```text
Usa find-skills para buscar skills de observabilidad.
```

### 2) `shapeup`

Usala para dirigir un ciclo Shape Up (framing, shaping, building, gates).

Ejemplos de uso:

```text
Usa shapeup start para iniciar un pitch de "alertas de parqueo en tiempo real".
```

```text
Usa shapeup status para revisar en que fase va el proyecto.
```

Nota: esta skill orquesta subcomandos como `/frame-coach`, `/shape`, `/plan`, `/breakdown` y `/hillchart`. Si alguno no existe en tu entorno, hay que instalarlo o ajustar el flujo.

### 3) `distributed-systems`

Usala cuando disenes o implementes comportamientos distribuidos:

- Idempotencia para endpoints criticos.
- Locks distribuidos.
- Circuit breaker y retry con backoff.
- Rate limiting distribuido.

Ejemplos de uso:

```text
Usa distributed-systems para implementar idempotencia en POST /api/payments en service-c.
```

```text
Usa distributed-systems para agregar circuit breaker y retry al cliente HTTP de service-a.
```

### 4) `clean-code`

Usala para revisar o refactorizar codigo buscando legibilidad y mantenibilidad.

Ejemplos de uso:

```text
Usa clean-code para hacer code review de gateway/main.py y listar hallazgos por severidad.
```

```text
Usa clean-code para refactorizar funciones largas y nombres ambiguos en service-b.
```

### 5) `documentation-writer`

Usala para crear documentacion estructurada (Tutorial, How-to, Reference, Explanation).

Ejemplos de uso:

```text
Usa documentation-writer para crear un How-to de despliegue local con Docker Compose.
```

```text
Usa documentation-writer para crear referencia de endpoints del gateway.
```

## Flujo recomendado para este repo

1. Disena cambios sensibles con `distributed-systems`.
2. Implementa y luego pasa `clean-code` para refactor final.
3. Documenta entregables con `documentation-writer`.
4. Si falta una capacidad, usa `find-skills` para instalar otra skill.

## Solucion de problemas

- Si una skill no se activa, nombrala en el prompt con su nombre exacto (`clean-code`, `distributed-systems`, etc.).
- Verifica que exista su carpeta en `.agents/skills/`.
- Si acabas de instalar skills nuevas, reinicia Codex para que las cargue.

