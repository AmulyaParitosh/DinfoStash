import firebase_admin
from firebase_admin import credentials, db, firestore, storage

from .config import SETTINGS

cred = credentials.Certificate(SETTINGS.serviceAccountCertificatePath)
firebase_app = firebase_admin.initialize_app(cred, SETTINGS.model_dump())

db = firestore.client(firebase_app)
users_collection = db.collection("users")

storage_bucket = storage.bucket(app=firebase_app)
