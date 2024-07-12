from app import app, db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4())
    name = db.Column(db.String)
    user_name = db.Column(db.String)
    mobile = db.Column(db.Integer)
    email = db.Column(db.String)
    salt = db.Column(db.String)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()