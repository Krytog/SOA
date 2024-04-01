from database.db_session import DBSession
from database.models import posts_table
from sqlalchemy import and_
import datetime


async def is_author(db: DBSession, post_id: int, user_id: int):
    query = posts_table.select().where(posts_table.c.id == post_id)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()[0]
    return result_as_dict["author"] == user_id


async def exists(db: DBSession, post_id: int):
    query = posts_table.select().where(posts_table.c.id == post_id)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()
    return len(result_as_dict) != 0


async def create_post(db: DBSession, user_id: int, content: str):
    create_time = datetime.datetime.now(datetime.timezone.utc)
    query = posts_table.insert().values(
        author_id=user_id,
        content=content,
        last_modified=create_time,
        created=create_time
    )
    result = await db.execute(query)
    await db.commit()
    return result.inserted_primary_key[0]


async def update_post(db: DBSession, post_id: int, new_content: str):
    query = posts_table.update().where(posts_table.c.id == post_id).values(
        content=new_content,
        last_modified=datetime.datetime.now(datetime.timezone.utc),
    )
    await db.execute(query)
    await db.commit()


async def delete_post(db: DBSession, post_id: int):
    query = posts_table.delete().where(posts_table.c.id == post_id)
    await db.execute(query)
    await db.commit()


async def get_post(db: DBSession, post_id: int):
    query = posts_table.select().where(posts_table.c.id == post_id)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()[0]
    return result_as_dict


async def get_posts_list(db: DBSession, user_id: int, page: int, per_page: int):
    query = posts_table.select().where(posts_table.c.author == user_id).order_by(
        posts_table.c.created.desc()).offset(page * per_page).limit(per_page)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()
    return result_as_dict
