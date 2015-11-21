import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLAlCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
SQLALCHEMY_MIGRATEREPO = os.path.join(basedir,'db_repository')
