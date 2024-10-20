import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os



class EmailSender:
    def __init__(self, email, app_password):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = email
        self.password = app_password

    def send_mail_with_attachment(self, body, title, receiver_email, file_path):
        # Criando a mensagem
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = os.getenv("EMAIL_SUBJECT", title)


        message.attach(MIMEText(body, "plain"))

        # Anexando um arquivo
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}",
            )

            message.attach(part)

            # Conectando ao servidor e enviando o email
            context = ssl.create_default_context()

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)  # Segurança na conexão
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())

            print("Email enviado com sucesso!")

        except FileNotFoundError:
            print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao enviar o email: {e}")
            
