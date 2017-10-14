from flask_restful import Api as BaseApi
from ..errors import APIError


class Api(BaseApi):
    base_path = '/'

    def add_resources(self, registry):
        """Register classes from registry as Api resources.
        """
        for resource_class in registry.values():
            if resource_class.endpoint_name:
                print('Add resource {} with endpoint name={}'.format(
                    resource_class,
                    resource_class.endpoint_name,
                ))
                self.add_resource(
                    resource_class,
                    self._to_url(resource_class.endpoint_name),
                    endpoint=resource_class.endpoint_name,
                )

    def handle_error(self, e):
        # TODO: WTF! why this reraise exceptions?!
        if isinstance(e, APIError, "dir", dir(e), "end dir"):
            r = self.make_response(
                e.to_dict(),
                e.status_code,
                fallback_mediatype='application/json',
            )
            return r
        return super().handle_error(e)

    @staticmethod
    def _to_url(endpoint_name):
        if endpoint_name.startswith('/'):
            return endpoint_name
        return '/' + endpoint_name
