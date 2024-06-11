from datetime import datetime

from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256

from ..db import db


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=True)
    phone_no = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_type = db.Column(db.Enum("user", "admin", "super_admin", name="user_type"),
                          default="user", nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    inactive_date = db.Column(db.DateTime)
    active_date = db.Column(db.DateTime, default=datetime.utcnow())

    audit = db.relationship("AuditModel", back_populates="user", lazy="dynamic")
    __table_args__ = (
        db.UniqueConstraint('phone_no', 'email', 'first_name', 'last_name'),
    )

    def get_id(self):
        return (self.id)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone_no(cls, phone_no):
        return cls.query.filter_by(phone_no=phone_no).first()
    def check_pwd(self, password):
        is_password_correct = pbkdf2_sha256.verify(password, self.password)
        return is_password_correct

    def make_inactive(self):
        self.is_active = False
        self.inactive_date = datetime.utcnow()
        self.save_to_db()

    def make_active(self):
        self.is_active = True
        self.active_date = datetime.utcnow()
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()
