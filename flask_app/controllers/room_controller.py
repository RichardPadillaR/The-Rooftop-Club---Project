from flask_app import app
from flask_app.models import  reservations_model, user_model
from flask import render_template, request, flash, session, redirect 

@app.route("/all_rooms")
def our_rooms ():
    if "user_id" not in session:
        flash("please log in to browse the website", "login")
        return redirect ("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        return render_template("all_rooms.html", user = user )

@app.route("/double_room")
def twin_room ():
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        user_id = session["user_id"]
        return render_template("double_room.html", user_id = user_id, user = user)

@app.route("/double_room", methods=["POST"])
def twin_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/double_room")

@app.route("/king_room")
def king_room ():
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        user_id = session["user_id"]
        return render_template("king_room.html", user_id = user_id, user = user)

@app.route("/king_room", methods = ["POST"])
def king_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/king_room")

@app.route("/suite_room")
def suite_room ():
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        user_id = session["user_id"]
        return render_template("suite_room.html", user_id = user_id, user = user)


@app.route("/suite_room", methods = ["POST"])
def suite_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/suite_room")


@app.route("/penthouse")
def penthouse ():
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        user_id = session["user_id"]
        return render_template("penthouse.html", user_id = user_id, user = user)

@app.route("/penthouse", methods = ["POST"])
def penthouse_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/penthouse")