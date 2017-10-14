from ..database import db


class Report(db.BaseModel):
    __tablename__ = 'reports'
    serializable_attrs = [
        'photo_id',
        'verdicts'
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    reason = db.Column(db.String, nullable=False)
    # json with Dict[user_id: verdict]
    verdicts = db.Column(db.String, nullable=False)

    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
