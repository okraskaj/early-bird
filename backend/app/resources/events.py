from ..db import models
from ..flask_restful_extensions import Resource


class EventsResource(Resource):
    endpoint_name = 'events'

    def get(self):
        """Get event by app_id."""
        event_id = self.request_json['event_id']
        event = models.Event.first_or_abort(app_id=event_id).to_dict()
        if any(self.request_json['user_id'] in [u.app_id
               for u in event.users_]):
            return event.to_dict()
        return 'You arent authorized to see this event!', 403

    def post(self):
        """Create new event.

        Example json:
        {
            "user_id": "niusadg213j21n32u321321",
            "name": "asdsada",
            "wakeup_hour": 340,
            "punish_points": 4,
            "main_punish": "asdsadsa dsadsad asd",
            "rules": [
                {"type": "punishment", "margin": 15, "points": 1},
                {"type": "punishment", "margin": 35, "points": 2},
                {"type": "cheating", "points": 3},
                {"type": "prize", "day_in_row": 3, "points": 1},
            ],
            "users": [
                "2321323123123123213fsdfds",
                "jsadhlsaudhsadusahdusadsa",
            ],
        }
        """
        rules = [models.Rule(**rule_dict)
                 for rule_dict in self.request_json.get('rules', [])]
        # TODO: invite new users (send them email to POST /users form
        users = list(models.User.query.filter(
            models.User.email.in_(self.request_json.get('users')),
        ).all())
        creator = models.User.first_or_abort(app_id=self.request_json['user_id'])
        # users.append(creator)
        event = models.Event(
            name=self.request_json['name'],
            creator_id=self.request_json['user_id'],
            hour=self.request_json['wakeup_hour'],
            punish_points=self.request_json['punish_points'],
            main_punish=self.request_json['main_punish'],
        ).save(commit=True)
        event.rules_.extend(rules)
        event.users_.extend(users)
        event.users_.append(creator)
        creator.event_id = event.id
        creator.event = event
        print(creator)
        creator.save(commit=True)
        return event.to_dict()
