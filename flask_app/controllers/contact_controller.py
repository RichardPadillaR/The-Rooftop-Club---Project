from flask_app import app
from flask import render_template, request, flash, session, redirect
import smtplib


@app.route("/contact")
def render_contact_us():
    return render_template("contact.html")

@app.route("/contact", methods=["POST"])
def contact_us():
    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()

    subject = request.form["subject"]
    body = request.form['message']
    sender = request.form["email"]
    recipients = ["fernandoadames2020@gmail.com", "fernanadoadames20222@gmail.com"]
    password = request.form["password"]

    send_email(subject, body, sender, recipients, password)
    return redirect("/")