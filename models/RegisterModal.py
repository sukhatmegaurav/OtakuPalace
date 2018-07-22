from pymongo import MongoClient
import bcrypt


class RegisterModal:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.otakupalace
        self.Users = self.db.users

    def insert_user(self, data):
        hashed_pass = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        id = self.Users.insert({"username": data.username, "first name": data.first_name,
                                "last name": data.last_name, "email": data.email,
                                "password": hashed_pass, "avatar": "", "background": "",
                                "User Info": {"favQuote": "", "education": "", "animeCount": 0, "currentAnime": "",
                                              "work": ""}})
        print("uid is", id)
