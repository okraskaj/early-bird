class APIError(Exception):
    def __init__(self, message, status_code=500, **kwargs):
        self.message = message or 'Server error.'
        self.status_code = status_code
        self.extra_kwargs = kwargs

    def to_dict(self):
        return {
            'message': self.message,
            **self.extra_kwargs
        }


class UserNotFoundError(APIError):
    def __init__(self, message=None):
        super().__init__(
            message or 'User with given ID not found.',
            status_code=404,
        )
