import aiosqlite
import re


async def create_db(): # функция создания базы данных
    async with aiosqlite.connect('ITSTech.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            name TEXT, 
                            study_group TEXT,
                            engineers_points INTEGER DEFAULT 0,
                            creative_points INTEGER DEFAULT 0
                        )
                        """)
        await db.commit()

async def check_registration(user_id: int): # функция проверки регистрации пользователя
    async with aiosqlite.connect('ITSTech.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE user_id = ?',(user_id,) )
        return await cursor.fetchone() is not None

async def validate_name(name): # регулярная проверка на ввод имени пользователя
    pattern = r'^(?=.*\S)([а-яА-ЯёЁ]+\s+){1,}[а-яА-ЯёЁ]+$'
    return bool(re.match(pattern, name)) and len(name) >= 2

async def validate_group(study_group): # регулярная проверка на ввод номера группы
    pattern = r'^[А-Яа-яЁё]{1,2}\d{1,2}-\d{2}[А-Яа-яЁё]$'
    return bool(re.match(pattern,study_group))

# функция добавления пользователя в базу данных
async def add_user(user_id: int, name: str, study_group: str, engineers_points: int, creative_points: int):
    async with aiosqlite.connect("ITSTech.db") as db:
        cursor = await db.execute("SELECT *  FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()

        if user is None:
            await db.execute("INSERT INTO users (user_id, name, study_group, engineers_points, creative_points) VALUES (?, ?, ?, ?, ?)", (user_id, name, study_group, engineers_points, creative_points))
            await db.commit()
            return True # Пользователь был добавлен
        else:
            return False # Пользователь уже добавлен

async def get_name_from_id(id: int): # функция получения Имени по айди
    async with aiosqlite.connect('ITSTech.db') as db:
        cursor = await db.execute('SELECT name FROM users WHERE user_id = ?', (id,))
        row = await cursor.fetchone()
        return row[0] if row else None


async def get_engineers_points(name: str): # получения баллов по имени
    async with aiosqlite.connect('ITSTech.db') as db:
        cursor = await db.execute('SELECT engineers_points FROM users WHERE name = ?', (name,))
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_creative_points(name: str): # получения баллов по имени
    async with aiosqlite.connect('ITSTech.db') as db:
        cursor = await db.execute('SELECT creative_points FROM users WHERE name = ?', (name,))
        row = await cursor.fetchone()
        return row[0] if row else None

async def add_engineers_points(name: str, points_to_add: int): # функция добавления инженерных баллов
    async with aiosqlite.connect('ITSTech.db') as db:
        await db.execute('UPDATE users SET engineers_points = engineers_points + ? WHERE name = ?', (points_to_add, name))
        await db.commit()

async def add_creative_points(name: str, points_to_add: int):# функция добавления креативных баллов
    async with aiosqlite.connect('ITSTech.db') as db:
        await db.execute('UPDATE users SET creative_points = creative_points + ? WHERE name = ?', (points_to_add, name))
        await db.commit()
