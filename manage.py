from flask_migrate import MigrateCommand
from flask_script import Manager

from demo.app import create_app
from demo.config import Config

app = create_app(config=Config())

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
