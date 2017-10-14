from uuid import uuid4

from ..database import db
from app.errors import UserNotFoundError


class User(db.BaseModel):
    __tablename__ = 'users'
    serializable_attrs = [
        'penalty_points',
        'name',
        # 'email',
        'app_id',
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    app_id = db.Column(
        db.String,
        nullable=False,
        unique=True,
        default=lambda: uuid4().hex,
    )
    penalty_points = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    event = db.relationship('Event', back_populates='users_')
    photos = db.relationship('Photo', back_populates='user')

    def to_dict(self):
        dict_ = super().to_dict()
        if self.event:
            dict_['event_id'] = self.event.app_id
        return dict_

    @classmethod
    def first_or_abort(cls, **kwargs):
        user = cls.query.filter_by(**kwargs).first()
        if user is None:
            raise UserNotFoundError('User with given id not found.')
        return user
