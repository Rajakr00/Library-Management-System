from flask_security import Security, SQLAlchemyUserDatastore
from .data.model import db , user, Role

security =  Security()
user_datastore = SQLAlchemyUserDatastore(db, user, Role)