from datetime import datetime

from ..db import db


class AuditModel(db.Model):
    __tablename__ = "audit_trail"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_update_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="audit")

