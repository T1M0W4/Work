import sqlite3

def view_users():
    """Извлекает и выводит всех пользователей из базы данных."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT phone_number, password FROM users')
    users = cursor.fetchall()
    conn.close()

    if users:
        for user in users:
            print(f"Phone Number: {user[0]}, Password: {user[1]}")
    else:
        print("No users found.")

# Вызов функции для отображения пользователей
view_users()
