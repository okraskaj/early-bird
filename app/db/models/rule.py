from ..database import db


class Rule(db.BaseModel):
    __tablename__ = 'rules'
    serializable_attrs = [
        'points',
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
    description = db.Column(db.String, nullable=False)
    time_margin = db.Column(db.Integer, nullable=True)
    days_in_row = db.Column(db.Integer, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __init__(
        self,
        points,
        description,
        time_margin=None,
        days_in_row=None,
    ):
        if (
            (days_in_row is None and time_margin is None) or
            (days_in_row is not None and time_margin is not None)
        ):
            raise ValueError(
                'Provide only one value: time_margin or days_in_row',
            )
        super().__init__(
            points=points,
            description=description,
            time_margin=time_margin,
            days_in_row=days_in_row,
        )

    def to_dict(self):
        result = super().to_dict()
        if self.days_in_row is not None:
            del result['time_margin']
            result['is_penalty'] = False
        else:
            del result['days_in_row']
            result['is_penalty'] = True
        return result
