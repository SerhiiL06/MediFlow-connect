from fastapi_mail import FastMail, MessageSchema

from core.settings.email import email_settings


class EmailService:
    def __init__(self):
        self.email = FastMail(email_settings.config)

    async def send_invation_link(self, email, token):
        link = f"http://127.0.0.1:8000/register/{token}"
        body = f"Click here for registration {link}"
        message = MessageSchema(
            subject="Registration for site",
            recipients=[email],
            body=body,
            subtype="html",
        )

        await self.email.send_message(message)
