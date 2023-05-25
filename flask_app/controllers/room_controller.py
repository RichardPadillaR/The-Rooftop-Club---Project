from flask_app import app
from flask_app.models import  reservations_model
from flask import render_template, request, flash, session, redirect 

@app.route("/all_rooms")
def our_rooms ():
    if "user_id" not in session:
        flash("Please log in to browse the website", "login")
        return redirect ("/")
    else:
        return render_template("all_rooms.html")

@app.route("/double_room")
def twin_room ():
    user_id = session["user_id"]
    return render_template("double_room.html", user_id = user_id)

@app.route("/double_room", methods=["POST"])
def twin_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/double_room")

@app.route("/king_room")
def king_room ():
    user_id = session["user_id"]
    return render_template("king_room.html", user_id = user_id)

@app.route("/king_room", methods = ["POST"])
def king_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/king_room")

@app.route("/suite_room")
def suite_room ():
    user_id = session["user_id"]
    return render_template("suite_room.html", user_id = user_id)


@app.route("/suite_room", methods = ["POST"])
def suite_room_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/suite_room")


@app.route("/penthouse")
def penthouse ():
    user_id = session["user_id"]
    return render_template("penthouse.html", user_id = user_id)

@app.route("/penthouse", methods = ["POST"])
def penthouse_reservation ():
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.save_reservation_form(request.form) 
        return redirect("/reservations")
    else:
        return redirect("/penthouse")