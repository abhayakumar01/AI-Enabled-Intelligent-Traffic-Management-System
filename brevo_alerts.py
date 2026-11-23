from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from urllib import error, request


class BrevoConfigurationError(ValueError):
    pass


class BrevoSendError(RuntimeError):
    pass


def send_confirmed_accident_email(
    image_path: str | Path,
    timestamp_seconds: float,
    frame_number: int,
    sender_email: str | None = None,
    recipient_emails: str | None = None,
) -> None:
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    sender = (sender_email or os.getenv("BREVO_SENDER_EMAIL", "")).strip()
    recipients = (recipient_emails or os.getenv("BREVO_RECIPIENT_EMAIL", "")).strip()

    if not api_key:
        raise BrevoConfigurationError("BREVO_API_KEY is not configured.")
    if api_key.startswith("xsmtpsib-"):
        raise BrevoConfigurationError("Use a Brevo API key, not an SMTP key.")
    if not sender:
        raise BrevoConfigurationError("BREVO_SENDER_EMAIL is not configured.")
    if not recipients:
        raise BrevoConfigurationError("BREVO_RECIPIENT_EMAIL is not configured.")

    snapshot = Path(image_path)
    if not snapshot.is_file():
        raise BrevoSendError(f"Incident snapshot not found: {snapshot}")

    recipient_list = [
        {"email": email.strip()}
        for email in recipients.replace(";", ",").split(",")
        if email.strip()
    ]
    if not recipient_list:
        raise BrevoConfigurationError("At least one recipient email is required.")

    content_type = mimetypes.guess_type(snapshot.name)[0] or "application/octet-stream"
    attachment = base64.b64encode(snapshot.read_bytes()).decode("ascii")
    payload = {
        "sender": {"email": sender, "name": "AI Traffic Management System"},
        "to": recipient_list,
        "subject": "Confirmed traffic accident detected",
        "htmlContent": (
            "<h2>Confirmed accident detected</h2>"
            f"<p>Timestamp: {timestamp_seconds:.1f} seconds</p>"
            f"<p>Frame: {frame_number}</p>"
            "<p>An incident snapshot is attached.</p>"
        ),
        "attachment": [
            {
                "name": snapshot.name,
                "content": attachment,
            }
        ],
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }
    http_request = request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=30) as response:
            if response.status not in (200, 201, 202):
                raise BrevoSendError(
                    f"Brevo returned HTTP {response.status}."
                )
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise BrevoSendError(
            f"Brevo rejected the email (HTTP {exc.code}): {detail}"
        ) from exc
    except error.URLError as exc:
        raise BrevoSendError(f"Could not reach Brevo: {exc.reason}") from exc
