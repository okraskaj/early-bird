from ..flask_restful_extensions import Resource


class HelloWorldResource(Resource):
    endpoint_name = 'hello-world'

    def get(self):
        return 'Hello World!'
