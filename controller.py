import web
from models import RegisterModal, UserLoginModel, PostPostsModel
import os

web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/postregistration', 'PostRegistration',
    '/userLogin', 'UserLogin',
    '/postUserLogin', 'PostUserLogin',
    '/logOut', 'Logout',
    '/postPostsPosting', 'PostPostsPosting',
    '/myProfile', 'MyProfile',
    '/accSettings', 'AccSettings',
    '/generalSettingsInfo', 'GeneralSettingsInfo',
    '/updateLike', 'UpdateLike',
    '/addCommentToPost', 'AddCommentToPost',
    '/upload-image/(.*)', "UploadImage"
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("gvs_sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("views/Templates", base="MainLayout", globals={'session': session_data,
                                                                            'current_user': session_data["user"]})


# Classes/Routes
class Home:
    def GET(self):
        # data = type('obj', (object,), {"username": "anushka_AA", "password": "anushka"})
        # is_correct = UserLoginModel.UserLoginModel().verify_credentials(data)
        # if is_correct:
        #     session_data["user"] = is_correct

        all_posts = PostPostsModel.PostPostsModel().get_all_posts()

        return render.Home(all_posts)


class Register:
    def GET(self):
        return render.Register()


class UserLogin:
    def GET(self):
        return render.UserLogin()


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None

        session.kill()
        return "success"


class MyProfile:
    def GET(self):
        # data = type('obj', (object,), {"username": "anushka_AA", "password": "anushka"})
        # is_correct = UserLoginModel.UserLoginModel().verify_credentials(data)
        # if is_correct:
        #     session_data["user"] = is_correct

        all_posts = PostPostsModel.PostPostsModel().get_user_posts(session_data['user']['username'])

        user = session_data["user"]

        return render.Profile(all_posts, user)


class AccSettings:
    def GET(self):
        # data = type('obj', (object,), {"username": "anushka_AA", "password": "anushka"})
        # is_correct = UserLoginModel.UserLoginModel().verify_credentials(data)
        # if is_correct:
        #     session_data["user"] = is_correct
        return render.Settings()


class PostRegistration:
    def POST(self):
        data = web.input()

        RegisterModal.RegisterModal().insert_user(data)
        return data.username


class PostUserLogin:
    def POST(self):
        data = web.input()
        verify = UserLoginModel.UserLoginModel()
        is_correct = verify.verify_credentials(data)

        if is_correct:
            session_data["user"] = is_correct
            return is_correct
        return "error"


class PostPostsPosting:
    def POST(self):
        data = web.input()
        current_user_name = session_data['user']['username']
        PostPostsModel.PostPostsModel().insert_post(data, current_user_name)
        return data.post


class GeneralSettingsInfo:
    def POST(self):
        data = web.input()
        current_user_name = session_data['user']['username']
        response = UserLoginModel.UserLoginModel().update_info(data, current_user_name)
        return response


class UpdateLike:
    def POST(self):
        data = web.input()
        response = PostPostsModel.PostPostsModel().updateLikes(data)
        return response


class AddCommentToPost:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']
        # print(data.user)
        # print(data.postID)
        # print(data.comment)
        response = PostPostsModel.PostPostsModel().addComment(data)
        if response:
            return response
        else:
            return "error 403"


class UploadImage:
    def POST(self, type):
        file = web.input(avatar={}, background={})

        file_dir = os.getcwd() + "\\static\\css\\uploads" + "\\" + session_data['user']['username']
        print(file_dir)

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "avatar" or "background" in file:
            filepath = file[type].filename
            filename = filepath.split('\\')[-1]
            f = open(file_dir + '\\' + filename, 'wb')
            f.write(file[type].file.read())
            f.close()

        update = {}
        update["type"] = type
        update["img"] = "/static/css/uploads/" + session_data['user']['username'] + '/' + filename
        update["username"] = session_data["user"]["username"]

        account_model = UserLoginModel.UserLoginModel()
        update_avatar = account_model.update_image(update)

        raise web.seeother("/myProfile")


if __name__ == "__main__":
    app.run()
