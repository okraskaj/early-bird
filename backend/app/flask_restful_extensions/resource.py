from collections import (
    defaultdict,
    Mapping,
)

from flask_restful import Resource as BaseResource

from flask import request
from flask.views import MethodViewType

from .register import (
    ClassRegister,
    ClassRegisterMeta,
)

API_RESOURCES_REGISTER = ClassRegister()
# store all resource classes in given ClassRegister instance.
ClassRegisterMeta.register = API_RESOURCES_REGISTER


class RedGuardianResourceMeta(ClassRegisterMeta, MethodViewType):
    pass


class Resource(BaseResource, metaclass=RedGuardianResourceMeta):
    endpoint_name = None

    def __init__(self, decorators=None, swager_spec=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._json = None
        if not self.endpoint_name.strip().startswith('/'):
            self.endpoint_name = '/' + self.endpoint_name.strip()
        self.method_decorators = defaultdict(list)
        if decorators:
            if isinstance(decorators, Mapping):
                self.add_method_decorator(**decorators)
            else:
                for decorator_kwargs in decorators:
                    self.add_method_decorator(**decorator_kwargs)

    @property
    def args(self):
        return request.args

    @property
    def request_json(self):
        if self._json is None:
            self._json = request.get_json()
        return self._json

    def add_method_decorator(
        self,
        decorator,
        http_method='post',
        request_decorator=True,
    ):
        http_method = http_method.lower()
        if not request_decorator:
            self.method_decorators[http_method].append(decorator)
        else:
            # first decorator always validate request data with swagger spec
            self.method_decorators[http_method].insert(1, decorator)
