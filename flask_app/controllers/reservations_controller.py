from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
from flask_app.models import reservations_model, user_model
from flask import render_template, request, flash, session, redirect 

@app.route("/reservations")
def reservation():
    if "user_id" not in session:
        flash("please log in to browse the website", "login")
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        user_id = session["user_id"]
        user = user_model.User.get_user_with_all_reservations(user_id)
        return render_template("reservations.html", all_users = user, user = user)

@app.route("/view/<room_name>")
def view_room(room_name):
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        if room_name == "The Grand Serenity":
            return render_template("view_double_room.html")
        elif room_name == "Luxe King Haven":
            return render_template("view_king_room.html")
        elif room_name == "The Diamond Skyline":
            return render_template ("view_penthouse.html")
        elif room_name == "The Royal Splendor":
            return render_template ("view_suite_room.html")
        else:
            return redirect("/reservations", user = user)

@app.route("/delete_reservation/<int:room_id>")
def delte_a_reservation(room_id):
    reservations_model.Reservations.delete_reservation(room_id)
    return redirect("/reservations")

@app.route("/edit/<room_name>/<int:reservation_id>")
def edit_reservation(room_name, reservation_id):
    if "user_id" not in session:
        return redirect("/")
    else:
        user = user_model.User.get_user_by_ID(session["user_id"])
        if room_name == "The Grand Serenity":
            reservation = reservations_model.Reservations.get_reservation_by_id(reservation_id)
            return render_template("edit_double_room.html", reservation = reservation)
        elif room_name == "Luxe King Haven":
            reservation = reservations_model.Reservations.get_reservation_by_id(reservation_id)
            return render_template("edit_king_room.html", reservation = reservation)
        elif room_name == "The Diamond Skyline":
            reservation = reservations_model.Reservations.get_reservation_by_id(reservation_id)
            return render_template ("edit_penthouse.html", reservation = reservation)
        elif room_name == "The Royal Splendor":
            reservation = reservations_model.Reservations.get_reservation_by_id(reservation_id)
            return render_template ("edit_suite_room.html", reservation = reservation, user = user)
        else:
            return redirect("/reservations")

@app.route("/edit/<room_name>/<int:reservation_id>", methods = ["POST"])
def update_reservation(room_name, reservation_id):
    if reservations_model.Reservations.validate_reservation(request.form):
        reservations_model.Reservations.update_reservation(request.form, reservation_id)
        return redirect("/reservations")
    else:
        return redirect(f"/edit/{room_name}/{reservation_id}")






