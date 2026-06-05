from distro import name
from flask import Blueprint, request, jsonify, session, render_template
from utils.firebase_admin import verify_token, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/verify-token', methods=['POST'])
def verify_user():
    data = request.get_json()

    print("📥 Incoming data:", data)

    id_token = data.get('token')
    name = data.get('name', 'Explorer')

    decoded = verify_token(id_token)

    if not decoded:
        return jsonify({"status": "error"}), 401

    print("🔍 Decoded token:", decoded)

    user_id = decoded['uid']
    session['user'] = user_id

    print("✅ Saving user:", user_id, name)

    # ✅ Firestore logic (FIXED)
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()

    if not doc.exists:
        user_ref.set({
            "name": name
        }, merge=True)

    print("✅ Saved to Firestore")

    return jsonify({"status": "success"})

# 🧾 Signup page route (ADD THIS)
@auth_bp.route('/signup')
def signup_page():
    return render_template('signup.html')

# 🚀 Onboarding Step 1
@auth_bp.route('/onboarding1')
def onboarding1():
    return render_template('onboarding1.html')

@auth_bp.route('/onboarding2')
def onboarding2():
    return render_template('onboarding2.html')

@auth_bp.route('/onboarding3')
def onboarding3():
    return render_template('onboarding3.html')

@auth_bp.route('/save-onboarding', methods=['POST'])
def save_onboarding():
    user_id = session.get('user')

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()

    # Extract clean level label
    raw_level = data.get("step2", "") or ""
    if "Beginner" in raw_level:
        level_clean = "Beginner"
    elif "Intermediate" in raw_level:
        level_clean = "Intermediate"
    elif "Advanced" in raw_level:
        level_clean = "Advanced"
    else:
        level_clean = "Beginner"

    db.collection('users').document(user_id).set({
        "interests": data.get("step1", []),
        "level": level_clean,
        "topics": data.get("step3", [])
    }, merge=True)

    return jsonify({"status": "saved"})


# 🔐 Login page route (optional but clean)
@auth_bp.route('/login')
def login_page():
    return render_template('login.html')

@auth_bp.route('/test-db')
def test_db():
    db.collection("test").add({"hello": "world"})
    return "ok"