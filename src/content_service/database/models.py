import sqlalchemy

metadata = sqlalchemy.MetaData()

posts_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("author_id", sqlalchemy.Integer),
    sqlalchemy.Column("content", sqlalchemy.String()),
    sqlalchemy.Column("last_modified", sqlalchemy.DateTime(timezone=True)),
    sqlalchemy.Column("created", sqlalchemy.DateTime(timezone=True))
)
