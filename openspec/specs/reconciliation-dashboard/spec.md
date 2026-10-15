# reconciliation-dashboard Specification

## Purpose
Proporciona una interfaz web moderna e interactiva para visualizar los resultados de la conciliación de datos, métricas clave, gráficos y discrepancias detalladas.

## Requirements

### Requirement: Visualización de métricas generales de auditoría
El panel web SHALL mostrar tarjetas con indicadores de resumen del proceso de conciliación ejecutado.

#### Scenario: Presentación de indicadores clave
- **WHEN** culmina el procesamiento de ambas tablas
- **THEN** el sistema muestra el total de registros analizados, el porcentaje de coincidencia, el total de coincidencias exactas, registros faltantes y total de discrepancias

### Requirement: Gráficos interactivos de estado de conciliación
La interfaz SHALL renderizar gráficos interactivos que muestren la proporción de registros correctos frente a registros con discrepancias o ausencias.

#### Scenario: Visualización del gráfico de distribución
- **WHEN** el usuario accede al panel de control con resultados de conciliación
- **THEN** el sistema despliega un gráfico visual que desglosa registros conciliados vs discrepantes vs no encontrados

### Requirement: Tabla interactiva de detalle de discrepancias
La interfaz SHALL incluir una tabla interactiva con capacidades de búsqueda, paginación y filtro para examinar cada registro en desacuerdo.

#### Scenario: Filtrado por tipo de discrepancia
- **WHEN** el usuario selecciona un filtro por columna con error o por registro faltante
- **THEN** la tabla actualiza sus filas para mostrar únicamente las inconsistencias correspondientes
