class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


CONFIG_MAPPING = {
    'develompment': DevConfig,
    'dev': DevConfig,
    'default': DevConfig,
}


def get_config(config_name):
    return CONFIG_MAPPING.get(config_name, CONFIG_MAPPING['default'])
