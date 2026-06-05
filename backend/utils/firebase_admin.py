import firebase_admin
from firebase_admin import credentials, auth, firestore

# 🔐 Load service account
cred = credentials.Certificate("firebase_config/serviceAccountKey.json")

# 🔥 Prevent duplicate initialization
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# ✅ ADD THIS (VERY IMPORTANT)
db = firestore.client()


# 🔐 VERIFY TOKEN
def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print("Token error:", e)
        return None