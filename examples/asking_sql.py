import aconsole
import asyncio
import sqlite3


DB = sqlite3.connect("users.db")
CMD = aconsole.AsyncConsole()

def init_db():
    cursor = DB.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, age INTEGER)')
    DB.commit()
    cursor.close()

def insert_user(name, age):
    cursor = DB.cursor()

    cursor.execute('INSERT INTO users VALUES(?, ?)', [name, age])
    DB.commit()
    cursor.close()

def fetch_users():
    cursor = DB.cursor()
    
    cursor.execute('SELECT * FROM users')
    for table in cursor.fetchall():
        name = table[0]
        age = table[1]

        CMD.print("Name: {%s}, Age:  {%s}"%(name, age))
        CMD.print("---------------------------------")

    cursor.close()

async def main():
    fetch_users()
    
    while True:
        name = await CMD.input("What is your name: ")
        age = 0
        
        while True:
            try:
                age = int((await CMD.input("What is your age: ")))
                break
            except:
                CMD.set_colors('black', 'red')
                await asyncio.sleep(1)
                CMD.set_colors('black', 'green')

        insert_user(name, age)
        
        CMD.clear_output()
        fetch_users()

        await asyncio.sleep(2)

if __name__ == '__main__':
    init_db()

    loop = asyncio.get_event_loop()

    run_task = CMD.run()
    loop.create_task(main())

    loop.run_until_complete(run_task)
