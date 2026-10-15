# 📊 Excel Reconciler & Auditor Dashboard

Sistema de conciliación inteligente de datos entre dos tablas de Excel con panel de control interactivo, detección de discrepancias celda a celda y alertas automáticas por correo electrónico. Diseñado e implementado siguiendo la metodología **Spec-Driven Development (SDD)** con **OpenSpec**.

---

## 🚀 Características Principales

- **Cruce Vectorizado de Tablas:** Cruce de archivos `.xlsx` y `.xls` mediante clave/ID común usando Pandas y openpyxl.
- **Detección y Clasificación de Incidencias:**
  - Registros faltantes en Tabla B (*Missing in B*).
  - Registros faltantes en Tabla A (*Missing in A*).
  - Diferencias de valores en columnas comparables (*Value Mismatch*).
- **Dashboard Web Interactivo:**
  - Tarjetas de métricas y tasa de coincidencia en tiempo real.
  - Gráficos interactivos de estado (donas y barras) con Chart.js.
  - Tabla dinámica con filtrado instantáneo por tipo de error y buscador textual.
- **Alertas Automáticas por Correo (SMTP):**
  - Plantilla responsiva en formato HTML enviada en segundo plano (*BackgroundTasks*).
  - Despacho condicional: solo se dispara si se confirman discrepancias.
- **Metodología OpenSpec:**
  - Todas las capacidades del sistema están formalizadas en `openspec/specs/` con requerimientos y escenarios BDD testables.

---

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.12, FastAPI, Uvicorn
- **Procesamiento de Datos:** Pandas, OpenPyXL
- **Frontend:** Jinja2, Tailwind CSS, Chart.js, FontAwesome
- **Servicio de Notificaciones:** Python Standard `smtplib`, `email.mime`
- **Testing:** Pytest (10 tests unitarios y de integración)
- **Metodología:** OpenSpec CLI

---

## 📦 Estructura del Proyecto

```text
excel-reconciliation-dashboard/
├── .agents/                 # Workflows y skills de OpenSpec para Antigravity
├── openspec/                # Fuente de verdad: especificaciones del sistema
│   ├── specs/               # Capacidades estables consolidadas
│   │   ├── alert-notifications/
│   │   ├── excel-reconciliation/
│   │   └── reconciliation-dashboard/
│   └── changes/archive/     # Historial de propuestas archivadas
├── reconciliation/          # Núcleo de lectura y conciliación
│   ├── reader.py
│   └── engine.py
├── notifications/           # Módulo de despacho de alertas SMTP
│   └── mailer.py
├── templates/               # Vistas HTML
│   ├── dashboard.html
│   └── email_alert.html
├── sample_data/             # Datos de prueba para testing
├── ejemplos_excel/          # Casos prácticos listos para probar
├── tests/                   # Suite completa de pruebas con pytest
├── config.py                # Configuración y variables de entorno
├── main.py                  # API FastAPI y servidor de vistas
└── requirements.txt         # Dependencias del proyecto
```

---

## ⚡ Inicio Rápido

### 1. Clonar e instalar dependencias
```bash
git clone https://github.com/Gerferru/excel-reconciliation-dashboard.git
cd excel-reconciliation-dashboard

python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar variables de entorno (Opcional para correo real)
Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```
Configura tus credenciales SMTP (por ejemplo, Gmail o SMTP corporativo).

### 3. Iniciar el servidor
```bash
uvicorn main:app --reload --port 8000
```
Abre en tu navegador: **[http://localhost:8000](http://localhost:8000)**.

---

## 🧪 Ejecutar Pruebas Automatizadas

```bash
pytest
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
