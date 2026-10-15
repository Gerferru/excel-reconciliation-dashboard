# excel-reconciliation Specification

## Purpose
Permite procesar y conciliar dos tablas de datos en formato Excel mediante una clave común, detectando automáticamente discrepancias de valores y registros faltantes.

## Requirements

### Requirement: Carga y lectura de dos tablas Excel
El sistema SHALL permitir cargar dos archivos o tablas en formato Excel (.xlsx, .xls) y extraer sus datos en estructuras tabulares para su posterior procesamiento.

#### Scenario: Carga exitosa de ambos archivos
- **WHEN** el usuario proporciona dos archivos Excel válidos con formato de tabla tabular
- **THEN** el sistema procesa ambas tablas e identifica sus columnas disponibles

#### Scenario: Archivo no válido o corrupto
- **WHEN** se proporciona un archivo con extensión no compatible o contenido ilegible
- **THEN** el sistema rechaza la operación e informa un error descriptivo

### Requirement: Conciliación de registros por clave única
El sistema SHALL cruzar los registros de ambas tablas utilizando una columna de clave o identificador único seleccionada por el usuario.

#### Scenario: Detección de claves ausentes en Tabla B
- **WHEN** un registro con una clave existe en la Tabla A pero no existe en la Tabla B
- **THEN** el sistema marca el registro como faltante en la Tabla B

#### Scenario: Detección de claves ausentes en Tabla A
- **WHEN** un registro con una clave existe en la Tabla B pero no existe en la Tabla A
- **THEN** el sistema marca el registro como faltante en la Tabla A

### Requirement: Detección de discrepancias en valores coincidentes
El sistema SHALL comparar las columnas equivalentes entre registros coincidentes por clave y marcar cualquier discrepancia de valor entre ambas tablas.

#### Scenario: Valores idénticos en columnas comparadas
- **WHEN** dos filas comparten la misma clave y todos sus campos comparables coinciden exactamente
- **THEN** el sistema clasifica el registro como totalmente conciliado

#### Scenario: Desacuerdo de valores en una o más columnas
- **WHEN** dos filas comparten la misma clave pero uno o más campos tienen valores distintos
- **THEN** el sistema clasifica el registro con estado de discrepancia e indica el valor de la Tabla A y el valor de la Tabla B
