from ..database import db


class Rule(db.BaseModel):
    __tablename__ = 'rules'
    serializable_attrs = [
        'points',
        'type',
        'description',
        'time_margin',
        'days_in_row',
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    points = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    time_margin = db.Column(db.Integer, nullable=True)
    days_in_row = db.Column(db.Integer, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __init__(
        self,
        type,
        points,
        description,
        time_margin=None,
        days_in_row=None,
    ):
        if (
            (time_margin is not None and type in ('cheating', 'prize')) or
            (days_in_row is not None and type in ('cheating', 'punishment'))
        ):
            raise ValueError(
                'Invalid Values!'
            )
        super().__init__(
            points=points,
            description=description,
            time_margin=time_margin,
            days_in_row=days_in_row,
            type=type,
        )

    def to_dict(self):
        result = super().to_dict()
        if self.days_in_row is not None:
            del result['time_margin']
        else:
            del result['days_in_row']
        return result
