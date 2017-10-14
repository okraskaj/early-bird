from uuid import uuid4

from ..database import db


class Photo(db.BaseModel):
    __tablename__ = 'photos'
    serializable_attrs = [
        'upload_time',
        'app_id',
        'path',
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    upload_time = db.Column(db.DateTime, nullable=False)
    path = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    app_id = db.Column(
        db.String,
        nullable=False,
        unique=True,
        default=lambda: uuid4().hex,
    )

    user = db.relationship('User', single_parent=True)
    event = db.relationship('Event', back_populates='photos')

    def to_dict(self, with_user=False, with_event=False):
        dict_ = super().to_dict()
        dict_['upload_time'] = str(dict_['upload_time'])
        if with_event:
            dict_['event_id'] = self.event.app_id
        if with_user:
            dict_['user_id'] = self.user.app_id
        return dict_
