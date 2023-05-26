from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
from flask_app.models import user_model
from flask import render_template, request, flash, session, redirect
from email.message import EmailMessage
import smtplib

@app.route("/contact")
def contact_form():
    if 'user_id' not in session:
        return("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        return render_template("contact.html", user = user)

@app.route("/contact", methods=["POST"])
def contact_us():
    if user_model.User.validate_contact_us_form(request.form):

        sender = 'fernandoadames2023@outlook.com'
        receivers = 'fernandoadames2020@gmail.com'

        msg = EmailMessage()
        msg['Subject'] = "Online Meeting"
        msg['From'] = sender
        msg['To'] = receivers
        msg.set_content(f"User: {request.form['email']} sent a message\n\nMessage content:\n{request.form['message']}")

        try:
            smtpObj = smtplib.SMTP('outlook.office365.com', 587)
            smtpObj.starttls()
            smtpObj.login(sender, "Engineering@1160")
            smtpObj.send_message(msg)         
            print ("Successfully sent email")
        except:
            print("Error: unable to send email")

        # sender = "fernandoadames2023@outlook.com"
        # reciever = "fernandoadames2020@gmail.com"
        # message = request.form["message"]
        # subject = request.form["subject"]

        # email = EmailMessage()
        # email["From"] = sender
        # email["To"] = reciever
        # email["Subject"] = subject
        # email.set_content(message)

        # Username:2911f6765d8749
        # Password:1188be9ebb817f

        # sender = "Private Person <from@example.com>"
        # receiver = "A Test User <to@example.com>"

        # message = f"""\
        # Subject: Hi Mailtrap
        # To: {receiver}
        # From: {sender}

        # This is a test e-mail message."""

        # with smtplib.SMTP("sandbox.smtp.mailtrap.io", 25) as server:
        #     server.login("2911f6765d8749", "1188be9ebb817f")
        #     server.sendmail(sender, receiver, message)
        
        # smtp = smtplib.SMTP("sandbox.smtp.mailtrap.io", port=587)
        # smtp.starttls()
        # smtp.login(sender, "Engineering@1160")
        # smtp.sendmail(sender, reciever, email.as_string())
        # smtp.quit()

        return redirect("/")

    else:
        return redirect("/contact")