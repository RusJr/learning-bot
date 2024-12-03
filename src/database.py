import sqlite3


# Подключение к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('responses.db')
    conn.row_factory = sqlite3.Row  # Возвращать строки в виде словарей
    return conn


# Создаем таблицу для хранения ответов, если она еще не создана
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        user_id INTEGER,
        question TEXT,
        answer TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def save_answer(user_id, question, answer):
    # Сохраняем ответ в базу данных
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO responses (user_id, question, answer) VALUES (?, ?, ?)',
        (user_id, question, answer),
    )
    conn.commit()
    conn.close()


def get_answers_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM responses')
    rows = cursor.fetchall()

    if rows:
        answers_text = 'Ответы пользователей:\n'
        for row in rows:
            answers_text += f'Пользователь {row[0]}:\n'
            answers_text += f'Вопрос: {row[1]}\nОтвет: {row[2]}\n\n'
        return answers_text
    else:
        return 'Ответов нет!'
