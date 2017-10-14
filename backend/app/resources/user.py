import uuid
import werkzeug
import os
from flask_restful import reqparse
from datetime import datetime

from app import config
from app.db import models
from ..flask_restful_extensions import Resource


class UserResource(Resource):
    endpoint_name = 'users'

    def get(self):
        email = self.args['email']
        # TODO: why it raise exception that user was not found?
        return models.User.first_or_abort(email=email).to_dict()

    def post(self):
        """Create new user."""
        name = self.request_json['name']
        email = self.request_json['email']
        user = models.User(email=email, name=name).save(commit=True)
        return user.to_dict()


class UserIDResource(Resource):
    endpoint_name = 'users/<string:id_>'

    def get(self, id_):
        """Get user by app_id."""
        return models.User.first_or_abort(app_id=id_).to_dict()


class UsersPhotosResource(Resource):
    endpoint_name = 'users/<string:id_>/photos'

    def get(self, id_):
        """Get given user last n photos."""
        n = int(self.args.get('n')) if self.args.get('n') else None
        user = models.User.first_or_abort(app_id=id_)
        photos = {'photos': [photo.to_dict() for photo in user.photos[:n]]}
        return photos

    def post(self, id_):
        """Create new photo for given user."""
        parse = reqparse.RequestParser()
        parse.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        imageFile = args['photo']
        extension = os.path.splitext(imageFile.filename)[1]
        image_path = str(config.FILE_STORAGE / (str(uuid.uuid4()) + extension))
        imageFile.save(image_path)
        user = models.User.first_or_abort(app_id=id_)
        event = user.event
        photo = models.Photo(
            upload_time=datetime.utcnow(),
            path=image_path,
            user=user,
            event=event,
        ).save(commit=True)
        return photo.to_dict(), 200
