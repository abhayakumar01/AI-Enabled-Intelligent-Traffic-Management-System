from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BREVO_ENDPOINT = "https://api.brevo.com/v3/smtp/email"


class BrevoConfigurationError(RuntimeError):
    pass


class BrevoSendError(RuntimeError):
    pass


def _split_emails(raw_value: str | None) -> list[str]:
    if raw_value is None:
        return []
    emails = []
    for item in raw_value.replace(";", ",").split(","):
        cleaned = item.strip()
        if cleaned:
            emails.append(cleaned)
    return emails


def send_confirmed_accident_email(
    image_path: str | Path,
    timestamp_seconds: float,
    frame_number: int,
    sender_email: str | None = None,
    recipient_emails: str | list[str] | None = None,
    sender_name: str | None = None,
) -> None:
    """Send one confirmed-accident snapshot through Brevo SMTP API."""
    api_key = os.getenv("BREVO_API_KEY")
    if api_key and api_key.strip().startswith("xsmtpsib-"):
        raise BrevoConfigurationError(
            "Brevo SMTP key detected. Please generate a Brevo API key in SMTP & API > API Keys and paste that value here."
        )
    sender_email = (sender_email or os.getenv("BREVO_SENDER_EMAIL") or "abhayajb999@gmail.com").strip()
    recipient_values = _split_emails(
        recipient_emails if isinstance(recipient_emails, str) else ",".join(recipient_emails or [])
    )
    if not recipient_values:
        recipient_values = _split_emails(os.getenv("BREVO_RECIPIENT_EMAIL"))
    sender_name = sender_name or os.getenv("BREVO_SENDER_NAME", "AI Traffic Management System")

    missing = [
        name
        for name, value in (
            ("BREVO_API_KEY", api_key),
            ("BREVO_SENDER_EMAIL", sender_email),
            ("BREVO_RECIPIENT_EMAIL", ", ".join(recipient_values)),
        )
        if not value
    ]
    if missing:
        raise BrevoConfigurationError(
            "Missing Brevo environment variable(s): " + ", ".join(missing)
        )

    snapshot = Path(image_path)
    if not snapshot.is_file():
        raise BrevoSendError(f"Incident snapshot does not exist: {snapshot}")

    if sender_email:
        os.environ["BREVO_SENDER_EMAIL"] = sender_email
    if recipient_values:
        os.environ["BREVO_RECIPIENT_EMAIL"] = ", ".join(recipient_values)

    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": email} for email in recipient_values],
        "subject": "Confirmed traffic accident detected",
        "htmlContent": (
            "<h2>Confirmed traffic accident</h2>"
            f"<p>Timestamp: {timestamp_seconds:.1f} seconds</p>"
            f"<p>Video frame: {frame_number}</p>"
            "<p>The confirmed incident snapshot is attached.</p>"
        ),
        "attachment": [
            {
                "name": snapshot.name,
                "content": base64.b64encode(snapshot.read_bytes()).decode("ascii"),
            }
        ],
    }
    request = Request(
        BREVO_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status < 200 or response.status >= 300:
                raise BrevoSendError(f"Brevo returned HTTP {response.status}")
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise BrevoSendError(f"Brevo returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise BrevoSendError(f"Could not connect to Brevo: {error.reason}") from error
