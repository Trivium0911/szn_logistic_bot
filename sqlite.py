import sqlite3 as sq


async def start_db():
    global db, cur
    db = sq.connect('database.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,"
                "name TEXT, company TEXT, address TEXT, phone TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY "
                "AUTOINCREMENT, user_id TEXT, deliver_address TEXT, "
                "collection_time TEXT, comments TEXT, date_created DATE, "
                "hour INTEGER)")
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


async def edit_deliver(state, user_id, hour):
    async with state.proxy() as data:
        cur.execute("INSERT INTO orders(user_id, deliver_address, "
                    "collection_time, comments, date_created, hour)"
                    " VALUES('{}', '{}', '{}', '{}', CURRENT_DATE, "
                    "'{}')".format(user_id, data['deliver_address'],
                    data['getting_time'], data['comments'], hour)
                    )
        db.commit()


def get_user_info(user_id) -> str:
    user_info = cur.execute("SELECT name, company, address, phone "
                            "FROM users WHERE user_id = "
                            "'{}'".format(user_id)).fetchall()
    return f"Имя:   {user_info[0][0]} \n" \
           f"Компания:   {user_info[0][1]} \n" \
           f"Адрес:   {user_info[0][2]} \n" \
           f"Телефон:   {user_info[0][3]} \n\n"





