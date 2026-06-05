from flask import Blueprint, render_template, redirect, url_for, session

# ✅ LANDING PAGE (default)
# from flask import Blueprint, render_template

# home_bp = Blueprint('home', __name__)

# @home_bp.route('/')
# def home():
#     # return render_template('home.html')
#     return render_template("home.html", active_page="home")
#     return render_template("daily_brief.html", active_page="daily")
#     # return render_template("opportunities.html", active_page="opportunities")

# # @home_bp.route("/logout")
# # def logout():
# #     return redirect("/")

# from flask import Blueprint, render_template, redirect
import json
import os

home_bp = Blueprint('home', __name__)

# ✅ Home Page
@home_bp.route('/')
def landing():
    return render_template("landing.html")

# ✅ HOME PAGE (after explore)
@home_bp.route('/home')
def home():
    from flask import session
    from utils.firebase_admin import db

    file_path = os.path.join("static", "data", "fallback_news.json")
    with open(file_path, "r", encoding="utf-8") as f:
        fallback_data = json.load(f)

    # ✅ Load user profile from Firestore
    user_name = "Explorer"
    user_level = "Beginner"
    user_topics = []
    user_domain = [] 

    user_id = session.get('user')
    if user_id:
        try:
            doc = db.collection('users').document(user_id).get()
            if doc.exists:
                profile = doc.to_dict()
                user_name = profile.get('name', 'Explorer')
                user_level = profile.get('level', 'Beginner')
                user_topics = profile.get('topics', [])
                user_domain = profile.get('interests', [])
        except Exception as e:
            print("⚠️ Could not load user profile:", e)

    return render_template(
        "home.html",
        active_page="home",
        fallback_data=fallback_data,
        user_name=user_name,
        user_level=user_level,
        user_topics=user_topics,
        user_domain=user_domain
    )

def get_user_data():
    from flask import session
    from utils.firebase_admin import db

    user_name = "Explorer"
    user_level = "Beginner"
    user_domain = []

    user_id = session.get('user')

    if user_id:
        try:
            doc = db.collection('users').document(user_id).get()
            if doc.exists:
                profile = doc.to_dict()
                user_name = profile.get('name', 'Explorer')
                user_level = profile.get('level', 'Beginner')
                user_domain = profile.get('interests', [])
        except:
            pass

    return user_name, user_level, user_domain
# @home_bp.route('/home')
# def home():
#     return render_template("home.html", active_page="home", fallback_data=FALLBACK_DATA)

# LOGIN PAGE
@home_bp.route('/login')
def login():
    return render_template("login.html")

# ✅ LOGOUT → back to landing
@home_bp.route('/logout')
def logout():
    session.clear()   # 🔥 THIS LINE IS CRITICAL
    return redirect(url_for('home.landing'))
# @home_bp.route('/logout')
# def logout():
#     return redirect(url_for('home.landing'))

# LOGOUT → recommended to clear session in auth_routes.py and then redirect here

# @home_bp.route('/logout')
# def logout():
#     session.clear()   # 🔥 important
#     return redirect(url_for('home.landing'))


# ✅ Daily Brief Page
# @home_bp.route('/daily-brief')
# def daily_brief():
#     from flask import session
#     from utils.firebase_admin import db

#     user_name = "Explorer"
#     user_level = "Beginner"

#     user_id = session.get('user')
#     if user_id:
#         try:
#             doc = db.collection('users').document(user_id).get()
#             if doc.exists:
#                 profile = doc.to_dict()
#                 user_name = profile.get('name', 'Explorer')
#                 user_level = profile.get('level', 'Beginner')
#         except:
#             pass

#     return render_template("daily_brief.html", active_page="daily", user_name=user_name, user_level=user_level)

@home_bp.route('/daily-brief')
def daily_brief():
    user_name, user_level, user_domain = get_user_data()

    return render_template(
        "daily_brief.html",
        active_page="daily",
        user_name=user_name,
        user_level=user_level,
        user_domain=user_domain
    )

@home_bp.route('/saved')
def saved_items():
    user_name, user_level, user_domain = get_user_data()

    return render_template(
        "saved.html",
        user_name=user_name,
        user_level=user_level,
        user_domain=user_domain
    )
# @home_bp.route('/saved')
# def saved_items():
#     from flask import session
#     from utils.firebase_admin import db

#     user_name = "Explorer"
#     user_level = "Beginner"
#     user_id = session.get('user')
#     if user_id:
#         try:
#             doc = db.collection('users').document(user_id).get()
#             if doc.exists:
#                 profile = doc.to_dict()
#                 user_name = profile.get('name', 'Explorer')
#                 user_level = profile.get('level', 'Beginner')
#         except:
#             pass

#     return render_template("saved.html", user_name=user_name, user_level=user_level)