# Proposal

## Why

Las organizaciones suelen manejar múltiples fuentes de datos o reportes en formato Excel (por ejemplo, registros contables vs. bancarios, o inventario teórico vs. físico) cuya discrepancia genera pérdidas de tiempo y errores operativos cuando se revisan de forma manual. Este proyecto automatiza la ingesta y comparación de dos tablas de Excel mediante identificadores clave, presenta los resultados en un panel de control interactivo en tiempo real y notifica inmediatamente por correo electrónico a los responsables cuando se detectan incongruencias o discrepancias.

## What Changes

- Creación de un motor de reconciliación en Python con Pandas para procesar dos tablas de Excel y comparar registros basados en un ID/clave común.
- Clasificación de discrepancias: registros faltantes en Tabla A, registros faltantes en Tabla B y diferencias de valores en columnas comparables.
- Desarrollo de un panel de control web moderno con FastAPI, Jinja2, Tailwind CSS y Chart.js para explorar métricas, gráficos de discrepancias y tablas interactivas con filtros.
- Implementación de un servicio de notificaciones por correo electrónico (SMTP) con plantilla HTML que envía alertas automáticas cuando se detectan discrepancias.
- Endpoint y mecanismo para cargar archivos Excel y disparar la auditoría bajo demanda.

## Capabilities

### New Capabilities

- `excel-reconciliation`: Ingesta y cruce de dos tablas de Excel por clave única, detectando diferencias de valores y registros ausentes.
- `reconciliation-dashboard`: Panel web visual para inspeccionar métricas de auditoría, gráficos de concordancia y detalle de registros discrepantes.
- `alert-notifications`: Servicio de envío de alertas por correo electrónico en formato HTML cuando existen discrepancias entre las dos tablas.

### Modified Capabilities

*(Ninguna. Es la creación inicial del sistema).*

## Impact

- **Código y Dependencias**: Nueva aplicación Python basada en `FastAPI`, `uvicorn`, `pandas`, `openpyxl`, `jinja2` y soporte estándar de `smtplib`.
- **APIs**: Endpoints REST para subida de archivos, ejecución de reconciliación y visualización del panel.
- **Configuración**: Variables de entorno para configuración del servidor SMTP (host, puerto, usuario, contraseña, remitente y destinatarios).
