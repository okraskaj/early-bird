from ..db import models
from ..flask_restful_extensions import Resource


class EventsResource(Resource):
    endpoint_name = 'events'

    def post(self):
        """Create new event.

        Example json:
        {
            "user_id": "niusadg213j21n32u321321",
            "wakeup_hour": 340,
            "rules": [
                {"type": "punishment", "time_margin": 15, "points": 1},
                {"type": "punishment", "time_margin": 35, "points": 2},
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
        users = models.User.query.filter(
            models.User.email.in_(self.request_json.get('users')),
        ).all()
        event = models.Event(
            name=self.request_json['name'],
            creator_id=self.request_json['user_id'],
            hour=self.request_json['wakeup_hour'],
        ).save(commit=True)
        event.rules_.extend(rules)
        event.users_.extend(users)
        return event.to_dict()


class EventsIDResource(Resource):
    endpoint_name = 'events/<string:event_id>'

    def get(self, event_id):
        """Get event by app_id."""
        event = models.Event.first_or_abort(app_id=event_id).to_dict()
        if any(self.request_json['user_id'] in [u.app_id
               for u in event.users_]):
            return event.to_dict()
        return 'You arent authorized to see this event!', 403
