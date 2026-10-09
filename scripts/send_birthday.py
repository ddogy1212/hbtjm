"""Birthday greeting to one preapproved recipient via configured email/SMS providers.

No contact scraping, unsolicited broadcasts, or Instagram DM automation.
Do not store private numbers, emails or API tokens in this public repository.
"""
import base64
import datetime as dt
import os
import smtplib
import ssl
import urllib.parse
import urllib.request
from email.message import EmailMessage
from zoneinfo import ZoneInfo


def env(name: str) -> str:
    return os.getenv(name, "").strip()


def birthday_today() -> bool:
    birthday = env("BIRTHDAY_MMDD")
    if len(birthday) != 5 or birthday[2] != "-":
        print("Skipping: set BIRTHDAY_MMDD as MM-DD under GitHub Actions variables.")
        return False
    try:
        dt.datetime.strptime("2000-" + birthday, "%Y-%m-%d")
    except ValueError:
        print("Skipping: BIRTHDAY_MMDD is not a valid MM-DD date.")
        return False
    today = dt.datetime.now(ZoneInfo("Asia/Seoul")).strftime("%m-%d")
    if today != birthday:
        print("Skipping: today is not the configured birthday (Asia/Seoul).")
        return False
    return True


def send_email() -> bool:
    to, user, password = env("TARGET_EMAIL"), env("SMTP_USER"), env("SMTP_PASSWORD")
    if not all((to, user, password)):
        print("Email not configured. Skipping email.")
        return False

    msg = EmailMessage()
    msg["Subject"] = "🎂 황재민 생일축하해!!!"
    msg["From"] = user
    msg["To"] = to
    msg.set_content("🎂 황재민 생일축하해! 🎉\n" * 20 + "\n생일 정말 축하해! 🥳🎁")
    host = env("SMTP_HOST") or "smtp.gmail.com"
    port = int(env("SMTP_PORT") or "465")
    with smtplib.SMTP_SSL(host, port, timeout=20, context=ssl.create_default_context()) as server:
        server.login(user, password)
        server.send_message(msg)
    print("One birthday email handed to the configured SMTP service.")
    return True


def send_sms() -> bool:
    to, sender = env("TARGET_PHONE"), env("TWILIO_FROM")
    sid, token = env("TWILIO_ACCOUNT_SID"), env("TWILIO_AUTH_TOKEN")
    if not all((to, sender, sid, token)):
        print("SMS not configured. Skipping SMS.")
        return False
    if not to.startswith("+") or not to[1:].isdigit():
        raise ValueError("TARGET_PHONE must be in E.164 format (e.g., +821012345678).")
    data = urllib.parse.urlencode({
        "To": to,
        "From": sender,
        "Body": "🎂 황재민 생일축하해!!! 🎉🎁 생일 정말 축하해! 🥳",
    }).encode()
    url = "https://api.twilio.com/2010-04-01/Accounts/" + urllib.parse.quote(sid) + "/Messages.json"
    credentials = base64.b64encode((sid + ":" + token).encode()).decode()
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Authorization": "Basic " + credentials,
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        if response.status < 200 or response.status >= 300:
            raise RuntimeError("SMS provider rejected request: " + str(response.status))
    print("One birthday SMS accepted by configured provider (delivery is not guaranteed).")
    return True


def main() -> None:
    if env("CONSENT_CONFIRMED").lower() != "yes":
        print("No send: consent has not been confirmed with CONSENT_CONFIRMED=yes.")
        return
    if not birthday_today():
        return
    email_sent = send_email()
    sms_sent = send_sms()
    if not email_sent and not sms_sent:
        print("No external sending providers configured. The website alone cannot auto-send messages.")


if __name__ == "__main__":
    main()
