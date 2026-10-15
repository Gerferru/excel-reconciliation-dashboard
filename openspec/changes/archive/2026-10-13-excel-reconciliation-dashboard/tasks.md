# Tasks

## 1. Configuración del proyecto y dependencias

- [x] 1.1 Crear `requirements.txt` con las librerías necesarias (`fastapi`, `uvicorn`, `pandas`, `openpyxl`, `jinja2`, `python-multipart`, `python-dotenv`) y verificar la estructura inicial del proyecto.
- [x] 1.2 Crear el archivo `.env.example` con la plantilla de configuración de correo SMTP (host, puerto, credenciales, remitente y destinatarios) y verificar su lectura mediante un módulo de configuración.

## 2. Motor de Reconciliación de Excel

- [x] 2.1 Implementar el módulo de lectura de tablas Excel (`reconciliation/reader.py`) para extraer DataFrames y verificar la detección de columnas y tipos de datos.
- [x] 2.2 Implementar el núcleo de conciliación (`reconciliation/engine.py`) que compare ambas tablas por clave única, identificando registros faltantes y desacuerdos celda a celda, y verificarlo mediante pruebas automatizadas con casos controlados.

## 3. Servicio de Notificaciones por Correo (SMTP)

- [x] 3.1 Diseñar la plantilla de correo en HTML (`templates/email_alert.html`) y el servicio de despacho SMTP (`notifications/mailer.py`), verificando el formateo del correo con métricas de discrepancias y la gestión de errores de conexión.
- [x] 3.2 Implementar la regla de negocio que condicione el envío exclusivamente a la presencia de discrepancias o ausencias y verificar su activación en segundo plano (`BackgroundTasks`).

## 4. Backend FastAPI y Panel Web

- [x] 4.1 Configurar la aplicación FastAPI (`app.py` o `main.py`) con endpoints para carga de archivos Excel (`/api/reconcile`), configuración de columnas clave y endpoints de estado, verificando las respuestas JSON esperadas.
- [x] 4.2 Construir el panel de control web (`templates/dashboard.html`) con Tailwind CSS y Chart.js conteniendo tarjetas de resumen, gráficos de concordancia y tabla interactiva con filtros y búsqueda, y verificar la visualización en el navegador.

## 5. Integración y datos de prueba

- [x] 5.1 Generar un script o dataset de prueba con dos archivos Excel (`sample_data/tabla_a.xlsx` y `sample_data/tabla_b.xlsx`) que incluyan casos de éxito, datos discrepantes y registros faltantes, verificando la consistencia de los datos.
- [x] 5.2 Ejecutar una prueba integral de extremo a extremo subiendo ambos archivos a través de la interfaz web y verificando la precisión de las métricas en el dashboard y el registro del envío de correo.

## Workflow follow-up

- Revisar la solución implementada con el usuario.
- Ejecutar `openspec validate excel-reconciliation-dashboard` para confirmar que las especificaciones concuerdan con la implementación.
- Archivar el cambio con `openspec archive excel-reconciliation-dashboard` tras la validación final.
