from flask_script import (
    Manager,
    Server,
)
from flask_migrate import (
    Migrate,
    MigrateCommand,
)

from app import app
from app.db import db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('run_api', Server())
manager.add_command('db', MigrateCommand)


if '__main__' == __name__:
    manager.run()
