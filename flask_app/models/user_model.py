import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import reservations_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.profile_pic = data["profile_pic"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.reservation = None

    @classmethod
    def save(cls, user_form_dict):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW()) "
        result = connectToMySQL("project_db").query_db(query, user_form_dict)
        return result

    @classmethod
    def get_user_by_ID(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user_dict = {
            "id": user_id
        }
        result = connectToMySQL("project_db").query_db(query, user_dict)
        return cls(result[0])

    @classmethod
    def checking_if_user_email_exists_in_DB(cls, form_data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        result = connectToMySQL("project_db").query_db(query, form_data)
        if len(result) > 0:
            return True
        else:
            return False

    @classmethod
    def checking_if_an_email_is_associated_with_a_user_in_DB(cls,form_dict):
        user_dict = {
            "email": form_dict["email"]
        }
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("project_db").query_db(query, user_dict)
        if len(result) < 1:
            return False
        else:
            return cls(result[0])

    @classmethod
    def get_user_with_all_reservations(cls, user_id):

        user_dict = {
            "id" : user_id
        }

        query = """SELECT * FROM users
                LEFT JOIN reservations_date 
                ON reservations_date.user_id = users.id
                WHERE users.id = %(id)s ORDER by arrival_date ASC"""

        result = connectToMySQL("project_db").query_db(query, user_dict)
        this_list = []
        for db_row in result:
            if db_row["reservations_date.id"] == None:
                break
            else:
                this_user = cls(db_row)
                reservation_dict = {
                    "id": db_row["reservations_date.id"],
                    "arrival_date": db_row["arrival_date"],
                    "departure_date": db_row["departure_date"],
                    "number_of_people":  db_row["number_of_people"],
                    "room_name": db_row["room_name"],
                    "created_at": db_row["reservations_date.created_at"],
                    "updated_at": db_row["reservations_date.updated_at"],
                    "user_id": db_row["user_id"]
                }
        

            this_reservation = reservations_model.Reservations(reservation_dict)
            this_user.reservation = this_reservation
            this_list.append(this_user)
        return this_list

    @classmethod
    def edit_user_profile(cls, form_dict):
        query = """UPDATE users 
        SET email = %(email)s, password = %(password)s
        WHERE id = %(id)s"""
        result = connectToMySQL("project_db").query_db(query, form_dict)
        return result

    @classmethod
    def set_profile_picture(cls, user_id, filename):
        query = """UPDATE users 
        SET profile_pic = %(filename)s
        WHERE id = %(user_id)s"""
        data = {
            "user_id": user_id,
            "filename": filename
        }
        result = connectToMySQL("project_db").query_db(query, data)
        return result

    @staticmethod
    def validate_registration(user_registraion_data):
        is_valid = True
        if len(user_registraion_data["first_name"]) == 0:
            flash("please submit a First Name", "register")
            is_valid = flash
        elif len(user_registraion_data["first_name"]) < 2:
            flash("First name must be greater than 2 characters", "register")
            is_valid = False
        if len(user_registraion_data["last_name"]) == 0:
            flash("please submit a Last Name", "register")
            is_valid = flash
        elif len(user_registraion_data["last_name"]) < 2:
            flash("Last name must be greater than 2 characters", "register")
            is_valid = False
        if len(user_registraion_data["email"]) == 0:
            flash("Please submit an Email", "register")
            is_valid = False
        elif  not EMAIL_REGEX.match(user_registraion_data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        elif User.checking_if_user_email_exists_in_DB(user_registraion_data):
            flash("email already in use", "register")
            is_valid = False
        if len(user_registraion_data["password"]) == 0:
            flash("Please submit a password", "register")
            is_valid = False
        elif len(user_registraion_data["password"]) < 8:
            flash("password must be 8 characters or more", "register")
            is_valid = False
        elif user_registraion_data["password"] != user_registraion_data["confirm_password"]:
            flash("confirmed password does not match password", "register")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_edit(update_form):
        is_valid = True
        if len(update_form["email"]) == 0:
            flash("Please submit a valid Email", "update_profile")
            is_valid = False
        elif  not EMAIL_REGEX.match(update_form['email']): 
            flash("Invalid email address!", "update_profile")
            is_valid = False
        if len(update_form["current_password"]) == 0:
            flash("Please submit your current password", "update_profile")
            is_valid = False
        elif not update_form["existing_password"]:
            flash("invalid current password", "update_profile")
            is_valid = False
        if len(update_form["new_password"]) == 0:
            flash("Please submit a new password", "update_profile")
            is_valid = False
        if len(update_form["confirm_new_password"]) == 0:
            flash("Please re-enter your new password in confirm password    ", "update_profile")
            is_valid = False
        elif len(update_form["new_password"]) < 8:
            flash("password must be 8 characters or more", "update_profile")
            is_valid = False
        elif update_form["new_password"] != update_form["confirm_new_password"]:
            flash("new password does not match confirm password", "update_profile")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_contact_us_form(contact_form):
        is_valid = True
        if len(contact_form["email"]) == 0:
            flash("Please submit a valid Email",  "contact")
            is_valid = False
        elif  not EMAIL_REGEX.match(contact_form['email']): 
            flash("Invalid email address!",  "contact")
            is_valid = False
        if len(contact_form["subject"]) == 0:
            flash ("please provide a subject for your message", "contact")
            is_valid = False
        elif len(contact_form["subject"]) < 3:
            flash ("your subject cannot be less than 3 characters", "contact")
        if len(contact_form["message"]) == 0:
            flash ("please provide a message", "contact")
        if len(contact_form["message"]) < 6:
            flash ("your message cannot be less than 6 characters", "contact")
        return is_valid