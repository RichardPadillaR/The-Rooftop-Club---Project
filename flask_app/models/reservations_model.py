from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Reservations:
    def __init__(self,data):
        self.id = data["id"]
        self.arrival_date = data["arrival_date"]
        self.departure_date = data["departure_date"]
        self.number_of_people = data["number_of_people"]
        self.room_name = data["room_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = None

    @classmethod
    def save_reservation_form(cls, form_dict):
        query = "INSERT INTO reservations_date (arrival_date, departure_date, number_of_people, room_name, created_at, updated_at, user_id) VALUES (%(arrival_date)s, %(departure_date)s , %(number_of_people)s, %(room_name)s, NOW(), NOW(), %(user_id)s) "
        result = connectToMySQL("project_db").query_db(query, form_dict)
        return result

    @classmethod
    def get_reservation_by_id(cls, room_id):
        query = "SELECT * FROM reservations_date WHERE id = %(id)s"
        reservation_dict = {
            "id": room_id
        }
        result = connectToMySQL("project_db").query_db(query, reservation_dict)
        return cls(result[0])

    @classmethod
    def update_reservation(cls, form_dict, reservation_id ):
        query = "UPDATE reservations_date SET arrival_date = %(arrival_date)s, departure_date = %(departure_date)s, room_name = %(room_name)s, number_of_people = %(number_of_people)s WHERE reservations_date.id = %(id)s"
        new_form_data = {
            "arrival_date": form_dict["arrival_date"],
            "departure_date": form_dict["departure_date"],
            "number_of_people": form_dict["number_of_people"],
            "room_name": form_dict["room_name"],
            "user_id": form_dict["user_id"],
            "id": reservation_id
        }
        result = connectToMySQL("project_db").query_db(query, new_form_data)
        return result

    @classmethod
    def delete_reservation(cls, reservation_id):
        query = "DELETE FROM reservations_date WHERE id = %(id)s"
        reservation_dict = {
            "id": reservation_id
        }
        result = connectToMySQL("project_db").query_db(query, reservation_dict)
        return result

    @staticmethod
    def validate_reservation(reservation_dict):
        is_valid = True
        if len(reservation_dict["arrival_date"]) == 0:
            flash("Please select an arrival date", "room")
            is_valid = False
        if len(reservation_dict["departure_date"]) == 0:
            flash("Please select an departure_date", "room")
            is_valid = False
        if int(reservation_dict["number_of_people"]) == 0:
            flash("please provide the number of people for this reservation", "room")
            is_valid = False
        return is_valid