from uuid import uuid4
from collections import namedtuple

from ..database import db

Time = namedtuple('Time', ['hours', 'minutes'])


class Event(db.BaseModel):
    __tablename__ = 'events'
    serializable_attrs = [
        'app_id',
        'wakeup_hour',
        'rules',
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = db.Column(db.String, nullable=False)
    app_id = db.Column(
        db.String,
        nullable=False,
        unique=True,
        default=lambda: uuid4().hex,
    )
    # TODO: always add creator to users
    creator_id = db.Column(db.Integer)
    hour = db.Column(db.Integer, nullable=False)

    rules_ = db.relationship('Rule', cascade='all, delete-orphan')
    users_ = db.relationship('User', back_populates='event')
    photos = db.relationship(
        'Photo',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    @property
    def base_hour(self):
        return Time(
            hours=self.hour // 60,
            minutes=self.hour % 60,
        )

    @property
    def rules(self):
        return [rule.to_dict() for rule in self.rules_]

    @property
    def wakeup_hour(self):
        return '{}:{}'.format(self.base_hour.hours, self.base_hour.minutes)

    def to_dict(self):
        dict_ = super().to_dict()
        dict_['users'] = [user.app_id for user in self.users_]
        return dict_
