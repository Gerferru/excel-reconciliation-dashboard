# Design

## Context

El sistema parte desde cero para dar solución al cruce y auditoría de datos provenientes de dos hojas de cálculo Excel. Ver `proposal.md` para la motivación general del cambio.

## Goals / Non-Goals

**Goals:**
- Proveer un motor de reconciliación en memoria con Pandas capaz de realizar cruces por identificador único y reportar discrepancias detalladas celda a celda.
- Ofrecer un backend en FastAPI que exponga tanto la API para la carga/procesamiento como la interfaz web interactiva.
- Proporcionar un panel de control limpio con Tailwind CSS y Chart.js que visualice el porcentaje de coincidencia y la lista filtrable de inconsistencias.
- Diseñar un módulo de correo desacoplado que despache alertas HTML vía SMTP en segundo plano (BackgroundTasks) cuando se confirmen desacuerdos.

**Non-Goals:**
- Persistencia prolongada en bases de datos relacionales externas (en esta versión los resultados se computan por sesión/ejecución).
- Edición o corrección manual de valores de celdas dentro del propio navegador.
- Soporte para formatos propietarios no tabulares de Excel.

## Decisions

### Decisión 1: Framework web con FastAPI
- **Elección**: FastAPI sobre Flask o Django.
- **Razón**: Proporciona soporte nativo para tareas asíncronas en segundo plano (`BackgroundTasks`, ideal para el envío de correos sin bloquear la interfaz), tipado estricto con Pydantic y documentación interactiva automática.
- **Alternativas consideradas**: Flask (más ligero pero sin soporte nativo de async y validación por esquema sin plugins adicionales).

### Decisión 2: Motor de conciliación con Pandas y openpyxl
- **Elección**: Pandas con `merge(how='outer')` para alinear registros por la columna de clave compartida.
- **Razón**: Permite comparar vectorialmente columnas con nombres compartidos o mapeados, detectando diferencias de valores (`!=`), nulos y registros presentes en una sola tabla de forma extremadamente rápida.
- **Alternativas consideradas**: Recorrido iterativo fila por fila con `openpyxl` (mucho más lento y propenso a errores de tipado numérico/fecha).

### Decisión 3: Arquitectura de interfaz con plantillas Jinja2 + Tailwind CSS + Chart.js
- **Elección**: Server-side rendering con Jinja2, estilos modernos vía Tailwind CSS y gráficos con Chart.js.
- **Razón**: Elimina la necesidad de configurar pipelines de empaquetado de frontend (Node/Vite/Webpack), manteniendo una experiencia visual pulida y moderna en un único servicio fácil de ejecutar.
- **Alternativas consideradas**: SPA independiente en React/Vue (introduce complejidad de dependencias y despliegue adicional innecesaria para esta fase inicial).

### Decisión 4: Módulo de alertas por correo con smtplib y plantillas HTML
- **Elección**: Biblioteca estándar `smtplib` con soporte TLS/SSL y configuración mediante archivo `.env` (`python-dotenv`).
- **Razón**: Cero dependencias externas adicionales para el correo; funciona con cualquier proveedor SMTP estándar (Gmail, Outlook, servidores corporativos).
- **Alternativas consideradas**: APIs de terceros (SendGrid, Resend) que requerirían suscripciones o claves externas obligatorias.

## Risks / Trade-offs

- **[Riesgo: Hojas de cálculo con encabezados inconsistentes o tipos mixtos]** → *Mitigación*: Normalizar los nombres de columnas (strip de espacios, minúsculas) y realizar conversión segura de tipos antes de evaluar discrepancias.
- **[Riesgo: Demoras en el envío de correos por latencia de red SMTP]** → *Mitigación*: Ejecutar el envío de alertas dentro de una `BackgroundTask` de FastAPI para que el usuario reciba la respuesta del panel de forma inmediata.
- **[Riesgo: Nombres de claves o columnas con nombres diferentes entre tablas]** → *Mitigación*: Permitir que la interfaz o el servicio acepte la especificación de la columna de clave primaria para la Tabla A y la Tabla B.
