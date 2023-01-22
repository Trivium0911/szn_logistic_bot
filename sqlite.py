import sqlite3 as sq


async def start_db():
    global db, cur
    db = sq.connect('database.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,"
                "name TEXT, company TEXT, address TEXT, phone TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders(order_id INT PRIMARY KEY, "
                "user_id TEXT, deliver_address TEXT, collection_time TEXT, "
                "comments TEXT, date_created DATE)")
    db.commit()


def check_user(user_id):
    user = cur.execute("SELECT 1 FROM users "
                       "WHERE user_id == '{}'".format(user_id)).fetchone()
    return user


async def create_user(user_id):
    user = cur.execute("SELECT 1 FROM users "
                       "WHERE user_id == '{}'".format(user_id)).fetchone()
    match user:
        case None:
            cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                        (user_id, '', '', '', ''))
            db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE users SET name = '{}', company = '{}', "
                    "address = '{}', phone = '{}' "
                    "WHERE user_id == '{}'".format(
                        data['name'], data['company'],
                        data['address'], data['phone'], user_id)
                    )
        db.commit()



