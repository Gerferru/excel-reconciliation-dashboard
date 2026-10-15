import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader

from config import settings
from reconciliation.engine import ReconciliationResult

logger = logging.getLogger(__name__)
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def render_alert_html(result: ReconciliationResult) -> str:
    """Renderiza el cuerpo HTML del correo a partir del resultado de la reconciliación."""
    template = jinja_env.get_template("email_alert.html")
    context = result.to_dict()
    return template.render(**context)


def send_discrepancy_email(
    result: ReconciliationResult,
    to_emails: Optional[list[str]] = None,
) -> dict[str, Any]:
    """
    Envía un correo con el resumen de discrepancias mediante SMTP.
    Devuelve un diccionario con el estado del envío.
    """
    recipients = to_emails or settings.EMAIL_TO
    if not recipients:
        msg = "No hay destinatarios configurados en EMAIL_TO."
        logger.warning(msg)
        return {"success": False, "message": msg}

    subject = f"{settings.EMAIL_SUBJECT_PREFIX} Discrepancias detectadas ({result.total_discrepancies} diferencias)"
    html_content = render_alert_html(result)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.EMAIL_FROM
    message["To"] = ", ".join(recipients)
    message.attach(MIMEText(html_content, "html"))

    # Guardar copia local del correo generado para inspección y depuración
    emails_dir = Path(__file__).resolve().parent.parent / "emails_enviados"
    emails_dir.mkdir(exist_ok=True)
    preview_file = emails_dir / "ultima_alerta.html"
    preview_file.write_text(html_content, encoding="utf-8")

    try:
        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=5)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=5)
            if settings.SMTP_USE_TLS:
                server.starttls()

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(settings.EMAIL_FROM, recipients, message.as_string())
        server.quit()

        logger.info(f"Correo de alerta enviado exitosamente a {recipients}")
        return {
            "success": True,
            "message": f"Alerta enviada exitosamente a {', '.join(recipients)}",
            "recipients": recipients,
            "preview_url": "/api/view-email",
        }
    except Exception as exc:
        err_msg = f"No se pudo conectar al servidor SMTP ({settings.SMTP_HOST}:{settings.SMTP_PORT}). Sin embargo, el correo HTML fue generado y puedes previsualizarlo."
        logger.warning(f"Error SMTP: {exc}")
        return {
            "success": False,
            "message": err_msg,
            "error": str(exc),
            "preview_url": "/api/view-email",
        }


def trigger_alert_if_discrepancies(result: ReconciliationResult) -> Optional[dict[str, Any]]:
    """
    Evalúa si existen discrepancias antes de enviar la alerta.
    Solo se dispara si result.has_discrepancies es True.
    """
    if not result.has_discrepancies:
        logger.info("Conciliación limpia (sin discrepancias). No se envía correo de alerta.")
        return {
            "success": True,
            "message": "Sin discrepancias detectadas; no se requirió alerta.",
            "alert_triggered": False,
        }

    status = send_discrepancy_email(result)
    status["alert_triggered"] = True
    return status
