import datetime as dt

from . import models
from .database import db


def populate_db():
    users = [
        models.User(name='random'),
        models.User(name='test'),
        models.User(name='admin'),
    ]
    rules = [
        models.Rule(
            points=1,
            description='So close to wake up on time!',
            time_margin=15,
        ),
        models.Rule(
            points=2,
            description='So close to wake up on time!',
            time_margin=30,
        ),
        models.Rule(
            points=1,
            description='So close to wake up on time!',
            days_in_row=3,
        ),
    ]
    db.session.add_all(users)
    db.session.add_all(rules)
    event = models.Event(
        name='wake-up-bitch!',
        creator_id=users[-1].id,
        hour=7*60,
        users_=users[:-1],
        rules_=rules,
    )
    photos = [
        models.Photo(
            upload_time=dt.datetime.utcnow(),
            path='./use0.jpeg',
            user=users[0],
            event=event,
        ),
        models.Photo(
            upload_time=dt.datetime.utcnow(),
            path='./use1.jpeg',
            user=users[1],
            event=event,
        ),
        models.Photo(
            upload_time=dt.datetime.utcnow(),
            path='./use_ad.jpeg',
            user=users[-1],
            event=event,
        ),
    ]
    db.session.add_all([event])
    db.session.add_all(photos)
    db.session.commit()
