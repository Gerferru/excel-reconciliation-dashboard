# alert-notifications Specification

## Purpose
Gestiona la generación y envío automático de alertas por correo electrónico cuando se detectan discrepancias o desacuerdos entre las tablas de datos.

## Requirements

### Requirement: Detección y activación automática de alerta
El sistema SHALL evaluar el resultado de la conciliación y activar el flujo de notificación por correo únicamente cuando exista al menos una discrepancia o registro no coincidente.

#### Scenario: Discrepancias encontradas tras la conciliación
- **WHEN** la auditoría finaliza con una o más discrepancias o registros ausentes
- **THEN** el sistema inicia el proceso de preparación y envío de la alerta por correo electrónico

#### Scenario: Conciliación limpia sin discrepancias
- **WHEN** la auditoría finaliza con un 100% de coincidencias sin desacuerdos
- **THEN** el sistema no dispara el envío de correos de alerta

### Requirement: Generación de correo con reporte resumido en HTML
El sistema SHALL componer un correo electrónico con formato HTML que incluya un resumen ejecutivo de las discrepancias encontradas.

#### Scenario: Contenido de la alerta
- **WHEN** se genera la alerta de discrepancias
- **THEN** el cuerpo del correo incluye las métricas clave, la lista o resumen de discrepancias destacadas y un enlace o referencia al panel de control

### Requirement: Configuración segura de parámetros SMTP
El sistema SHALL obtener los parámetros de conexión SMTP (servidor, puerto, credenciales, remitente y destinatarios) a partir de variables de entorno configuradas.

#### Scenario: Configuración válida y envío satisfactorio
- **WHEN** los parámetros SMTP están configurados correctamente y se dispara una alerta
- **THEN** el correo es transmitido a la lista de destinatarios y se registra el resultado exitoso
