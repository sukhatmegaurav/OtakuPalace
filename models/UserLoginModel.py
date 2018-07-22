import pymongo
from pymongo import MongoClient
import bcrypt


class UserLoginModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.otakupalace
        self.Users = self.db.users

    def verify_credentials(self, data):
        intended_user = self.Users.find_one({"username": data.username})
        if intended_user:
            if bcrypt.checkpw(data.password.encode(), intended_user["password"]):
                return intended_user
            else:
                return False
        else:
            return False

    def update_info(self, data, current_user_name):
        updated = self.Users.update_one({
            "username": current_user_name
        }, {"$set": {"User Info": data}})
        return True

    def get_user(self, current_user_name):
        user = self.Users.find_one({"username": current_user_name})
        return user

    def update_image(self, update):
        updated = self.Users.update_one({"username": update["username"]},
                                        {"$set": {update["type"]: update["img"]}})
        return updated
