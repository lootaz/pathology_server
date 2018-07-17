import datetime
from flask import current_app, session

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseEntity(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_ts = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(255), nullable=False)

    def __init__(self):
        creator_name = current_app.config.get('SYSTEM_USER_NAME')

        self.create_ts = datetime.datetime.now()
        self.created_by = creator_name


class PathologyImage(BaseEntity):
    __tablename__ = 'ps_pathology_image'

    path = Column(String(512), nullable=False)

    def __init__(self, path):
        super().__init__()
        self.path = path


class PathologyType(BaseEntity):
    __tablename__ = 'ps_pathology_type'

    name = Column(String(255), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name


class PathologySelection(BaseEntity):
    __tablename__ = 'ps_pathology_selection'

    p1x = Column(Integer, nullable=False)
    p1y = Column(Integer, nullable=False)
    p2x = Column(Integer, nullable=False)
    p2y = Column(Integer, nullable=False)

    pathology_image_id = Column(Integer, ForeignKey('ps_pathology_image.id'), nullable=False)
    pathology_image = relationship('PathologyImage', backref=backref('pathology_selections', lazy='dynamic'))

    pathology_type_id = Column(Integer, ForeignKey('ps_pathology_type.id'), nullable=False)
    pathology_type = relationship("PathologyType")

    def __init__(self, p1x, p1y, p2x, p2y):
        super().__init__()

        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y
