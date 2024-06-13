import sqlite3

DB_NAME = 'listss.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, task STRING)''')

    conn.commit()
    conn.close()

# def add_task(user_id, username, task):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO tasks (user_id, username, task) VALUES (?,?,?)", (user_id, username, task))
#     conn.commit()
#     conn.close()


def add_task(user_id, username, task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the task already exists for the given user
    if not task_exists(user_id, task):
        cursor.execute("INSERT INTO tasks (user_id, username, task) VALUES (?,?,?)", (user_id, username, task))

    conn.commit()
    conn.close()

def get_task():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, username, task FROM tasks" )
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_tasks(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def update_task_id(old_id, new_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET id = ? WHERE id = ?", (new_id, old_id))

    conn.commit()

def task_exists(user_id, task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id =? AND task =?", (user_id, task))
    if cursor.fetchone():
        return True
    else:
        return False


def get_tasks(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id =?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def delete_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()

