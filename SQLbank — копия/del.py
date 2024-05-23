import sqlite3

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Удаляем все значения из таблицы "money"
cursor.execute("DELETE FROM money")

conn.commit()
print("Все записи из таблицы money удалены.")

# Закрываем соединение с базой данных
conn.close()
