from flask_restful import reqparse

from ..db import models
from ..flask_restful_extensions import Resource


class UserResource(Resource):
    endpoint_name = 'users'

    def post(self):
        """Create new user."""
        name = self.request_json['name']
        user = models.User(name=name).save(commit=True)
        return user.to_dict()


class UserIDResource(Resource):
    endpoint_name = 'users/<string:user_id>'

    def get(self, user_id):
        """Get user by app_id."""
        return models.User.first_or_abort(app_id=user_id).to_dict()


class UsersPhotosResource(Resource):
    endpoint_name = 'users/<string:user_id>/photos'

    def get(self, user_id):
        """Get given user last n photos."""
        n = int(self.args.get('n')) if self.args.get('n') else None
        user = models.User.first_or_abort(app_id=user_id)
        photos = {'photos': [photo.to_dict() for photo in user.photos[:n]]}
        return photos

    def post(self, user_id):
        """Create new photo for given user."""
        # TODO: add files posting
        pass
