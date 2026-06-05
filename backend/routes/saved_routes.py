# from flask import Blueprint, render_template

# saved_bp = Blueprint('saved', __name__)

# @saved_bp.route('/saved')
# def saved_page():
#     # 🔥 TEMP DATA (replace with Firebase later)
#     saved_articles = []
#     saved_flashcards = []

#     return render_template(
#         "saved.html",
#         saved_articles=saved_articles,
#         saved_flashcards=saved_flashcards
#     )
from flask import Blueprint, render_template, session

saved_bp = Blueprint('saved', __name__)

@saved_bp.route('/saved')
def saved_items():
    from utils.firebase_admin import db

    user_name = "Explorer"
    user_level = "Beginner"
    user_id = session.get('user')

    if user_id:
        try:
            doc = db.collection('users').document(user_id).get()
            if doc.exists:
                profile = doc.to_dict()
                user_name = profile.get('name', 'Explorer')
                user_level = profile.get('level', 'Beginner')
        except:
            pass

    return render_template("saved.html", user_name=user_name, user_level=user_level)