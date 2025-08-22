from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)


GMAIL_USER = "davidlaborda.2000@gmail.com"
GMAIL_PASSWORD = "wpsg akpz hrwh ggah"

@app.route('/send', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get("subject", "Sin comida")
    message = data.get("message", "El perro se quedo sin comida.")
    to = data.get("to", "davidlaborda.2000@gmail.com")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        return {"status": "Correo enviado"}, 200
    except Exception as e:
        return {"status": "Error", "detail": str(e)}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
