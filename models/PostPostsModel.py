import datetime

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import humanize


class PostPostsModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.otakupalace
        self.Users = self.db.users
        self.Posts = self.db.posts
        self.Comments = self.db.comments

    def insert_post(self, data, current_user_name):
        self.Posts.insert({"username": current_user_name, "content": data.post, "date_added": datetime.datetime.now(),
                           "like": 0})

    def get_all_posts(self):
        all_posts = self.Posts.find().sort('date_added', pymongo.DESCENDING)
        new_posts = []
        for post in all_posts:
            post["user"] = self.Users.find_one({"username": post["username"]})
            post["timestamp"] = humanize.naturaltime(datetime.datetime.now() - post["date_added"])
            new_posts.append(post)
            old_comments = self.Comments.find({"post_id": str(post["_id"])})
            post["comments"] = []
            for comment in old_comments:
                comment["user"] = self.Users.find_one({"username": comment["username"]})
                comment["timestamp"] = humanize.naturaltime(datetime.datetime.now() - comment["date_added"])
                post["comments"].append(comment)

        return new_posts

    def get_user_posts(self, current_user_name):
        all_posts = self.Posts.find({"username": current_user_name}).sort('date_added', pymongo.DESCENDING)
        new_posts = []
        for post in all_posts:
            post["user"] = self.Users.find_one({"username": post["username"]})
            post["timestamp"] = humanize.naturaltime(datetime.datetime.now() - post["date_added"])
            new_posts.append(post)
            old_comments = self.Comments.find({"post_id": str(post["_id"])})
            post["comments"] = []
            for comment in old_comments:
                comment["user"] = self.Users.find_one({"username": comment["username"]})
                comment["timestamp"] = humanize.naturaltime(datetime.datetime.now() - comment["date_added"])
                post["comments"].append(comment)

        return new_posts

    def updateLikes(self, data):
        post = self.Posts.find_one({"_id": ObjectId(data['num'])})
        post["like"] = post["like"] + 1
        handle = self.Posts.update_one({"_id": ObjectId(data['num'])}, {"$set": {"like": post["like"]}})
        return True

    def addComment(self, data):
        # inserted = self.Posts.update_one({"_id": ObjectId(data.postID)}, {"$push": {"comments": data}})
        inserted = self.Comments.insert({"post_id": data.postID, "comment_text": data.comment,
                                         "date_added": datetime.datetime.now(), "username": data.username})
        return inserted
