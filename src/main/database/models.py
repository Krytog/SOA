import sqlalchemy

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("login", sqlalchemy.String(50), unique=True, index=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column("email", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String(20)),
    sqlalchemy.Column("surname", sqlalchemy.String(20)),
    sqlalchemy.Column("birthdate", sqlalchemy.DateTime()),
    sqlalchemy.Column("phone", sqlalchemy.String(15)),
    sqlalchemy.Column("bio", sqlalchemy.String(500))
)

tokens_table = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("token", sqlalchemy.String(), index=True),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
    sqlalchemy.Column("owner", sqlalchemy.ForeignKey("users.id"))
)
