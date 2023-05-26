from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
from flask_app.models import user_model
from flask import render_template, request, flash, session, redirect 


@app.route("/")
def home ():
    if "user_id" not in session:
        return render_template("index.html")
    else:
        user_id = session["user_id"]
        user = user_model.User.get_user_by_ID(user_id)
        return render_template("index.html", user_id = int(user_id), user = user)

@app.route("/registration")
def registration():
    return render_template("register.html")

@app.route("/login")
def log_in ():
    return render_template("login.html")


@app.route("/registration", methods=["POST"])
def validate_registration_then_save_user_registration_in_DB():
    if  user_model.User.validate_registration(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        user_form_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
        }
        user_model.User.save(user_form_data)
        return redirect("/login")
    else:
        return redirect("/registration")


@app.route("/login", methods=["POST"])
def validate_login_then_log_in_a_user():
    this_user = user_model.User.checking_if_an_email_is_associated_with_a_user_in_DB(request.form)
    if not this_user:
        flash("invalid email or password", "login")
        return redirect("/login")
    if not bcrypt.check_password_hash(this_user.password, request.form["password"]):
        flash("invalid password", "login")
        return redirect("/login")
    session["user_id"] = this_user.id
    return redirect ("/")



@app.route('/update/form')
def updating_form_info():
    if "user_id" not in session:
        return redirect("/")
    else:
        return render_template("update_form.htnml")


@app.route("/logout")
def logging_out_user():
    session.pop("user_id")
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit_profile():
    current_user = user_model.User.get_user_by_ID(session["user_id"])
    file = request.files['profile_pic']
    file.save('flask_app/static/images/pic.jpg')
    profile_pic = 'static/images/pic.jpg'
    session["profile_pic"] = profile_pic
    check_password = bcrypt.check_password_hash(current_user.password, request.form["current_password"])
    new_dict = {
        "email":request.form["email"],
        "current_password": request.form["current_password"],
        "new_password": request.form["new_password"],
        "confirm_new_password": request.form["confirm_new_password"],
        "existing_password": check_password
    }
    if  user_model.User.validate_edit(new_dict):
        pw_hash = bcrypt.generate_password_hash(request.form['new_password'])
        user_form_data = {
        "email": request.form["email"],
        "password": pw_hash,
        "id": request.form["user_id"]
        }
        user_model.User.edit_user_profile(user_form_data)
        return redirect("/")
    else:
        return redirect("/edit")



@app.route("/edit")
def render_edit():
    user = user_model.User.get_user_by_ID(session["user_id"])
    return render_template("edit_profile.html", user_id = session["user_id"], user = user)




