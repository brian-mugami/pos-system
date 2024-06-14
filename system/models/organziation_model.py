from datetime import datetime

from ..db import db


class OrganizationModel(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    active_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="organizations")
    inventory = db.relationship("InventoryModel", back_populates="organization",
                                lazy="dynamic", secondary="organization_structure")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class InventoryModel(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    active_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="inventories")
    organization = db.relationship("OrganizationModel", back_populates="inventory", secondary="organization_structure")
    sub_inventory = db.relationship("SubInventoryModel", back_populates="inventory",
                                    lazy="dynamic", secondary="organization_structure")
    __table_args__ = (
        db.UniqueConstraint('name', 'organization_id'),
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name, id: int = None):
        if id is None:
            return cls.query.filter_by(name=name).all()
        else:
            return cls.query.filter_by(name=name, organization_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class SubInventoryModel(db.Model):
    __tablename__ = "sub_inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    active_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="sub_inventories")
    inventory = db.relationship("InventoryModel", back_populates="sub_inventory", secondary="organization_structure")

    __table_args__ = (
        db.UniqueConstraint('name', 'inventory_id'),
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name, id: int = None):
        if id is None:
            return cls.query.filter_by(name=name).all()
        else:
            return cls.query.filter_by(name=name, inventory_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class OrganizationStructureModel(db.Model):
    __tablename__ = "organization_structure"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False)
    sub_inventory_id = db.Column(db.Integer, db.ForeignKey("sub_inventory.id"), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    update_date = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('organization_id', 'inventory_id', 'sub_inventory_id'),
    )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        self.update_date = datetime.utcnow()
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
