import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('data.db')
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute('CREATE TABLE IF NOT EXISTS singUp(user TEXT, description TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS pay(id TEXT, username TEXT, photo TEXT, price TEXT)')
    base.commit()
 
async def sql_write_sing(us, data):
    values_list = data
    my_string = '\n'.join(values_list)
    print((us,my_string))
    cur.execute('INSERT INTO singUp (user, description) VALUES (?, ?)', (us,my_string))
    base.commit()

async def sql_read_sing():
    cur.execute('SELECT * FROM singUp')
    rows = cur.fetchall()
    return rows

async def sql_write_pay(id, us, arr):
    data = arr[1]
    price = arr[0]
    cur.execute('INSERT INTO pay (id, username, photo, price) VALUES (?, ?, ?, ?)', (id, us, data, price))
    base.commit()

async def sql_read_pay():
    cur.execute('SELECT * FROM pay')
    rows = cur.fetchall()
    return rows

async def sql_delete_pay(id):
    cur.execute('DELETE FROM pay WHERE id = ?', (id,))
    base.commit()