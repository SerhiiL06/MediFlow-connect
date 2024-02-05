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

    async def send_user_creditables(self, email, password):
        body = f"Your record was register successfully, your times creditabples are: -email {email} -password {password}"

        message = MessageSchema(
            subject="Record was register",
            recipients=[email],
            body=body,
            subtype="html",
        )

        await self.email.send_message(message)

    async def send_success_message(self, email):
        body = "Anything new"

        message = MessageSchema(
            subject="PubSub in move",
            recipients=[email],
            body=body,
            subtype="html",
        )

        await self.email.send_message(message)

    async def send_notification_about_opinion(self, email):
        body = "Dear client, your opinion is ready, please log into your profile and check this"

        message = MessageSchema(
            subject="Opinion", recipients=[email], body=body, subtype="html"
        )

        await self.email.send_message(message)
