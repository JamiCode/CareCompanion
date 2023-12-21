import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class User(_database.Base):
    __tablename__ = "users"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    first_name = _sql.Column(_sql.String)  # New column for first name
    last_name = _sql.Column(_sql.String)   # New column for last name
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    profile_picture = _sql.Column(_sql.String)  # Adjust the type as needed

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

    def __repr__(self) -> str:
        return f"User Record {self.first_name} {self.last_name}"
