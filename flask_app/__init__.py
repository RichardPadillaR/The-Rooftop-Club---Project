from flask import Flask
import os

app = Flask (__name__)
app.secret_key = "Keep this a secret"


app.config["UPLOAD_DIR"] = os.path.join(app.instance_path, "uploads")

# Create the upload dir if it doesn't exist
os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)