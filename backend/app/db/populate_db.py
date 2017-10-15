import datetime as dt

from . import models
from .database import db


def populate_db():
    users = [
        models.User(
            name='John',
            email="john26@cfc.en",
            app_id="8bb2f425777242e9942379ae5f92896d",
        ),
        models.User(
            name='Ola',
            email="ola.sk@protonmail.com",
            app_id="495787cf9b68458b93d668d9a71fc890",
        ),
        models.User(
            name='Janek',
            email="jan.g@gmail.com",
            app_id="d85b803f33fe4476970897b234a46248",
        ),
        models.User(
            name='Lukasz',
            email="lukasz@op.pl",
            app_id="89ca27d1d2c24ebb91fed6daf90bbc59",
        ),
    ]
    rules = [
        models.Rule(
            type='punishment',
            points=1,
            time_margin=15,
        ),
        models.Rule(
            type='punishment',
            points=2,
            time_margin=30,
        ),
        models.Rule(
            type='prize',
            points=1,
            days_in_row=3,
        ),
        models.Rule(
            type='cheating',
            points=1,
        ),
    ]
    db.session.add_all(users)
    db.session.add_all(rules)
    event = models.Event(
        name='wake-up-b****!',
        creator_id=users[-1].id,
        hour=7*60,
        main_punish='Buy coffee bonbon for everyone!.',
        punish_points=4,
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
            path='./use2.jpeg',
            user=users[2],
            event=event,
        ),
        models.Photo(
            upload_time=dt.datetime.utcnow(),
            path='./use_ad.jpeg',
            user=users[-1],
            event=event,
        ),
    ]
    event.users_.append(users[-1])
    db.session.add(event)
    db.session.add_all(photos)
    db.session.commit()
