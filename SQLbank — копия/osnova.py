import sqlite3


def add_record(conn, cursor, table_name):
    if table_name not in ['Clients', 'Accounts', 'Transactions', 'Employees', 'Loans', 'money']:
        print("Неверное имя таблицы.")
        return

    columns = []
    cursor.execute("PRAGMA table_info({})".format(table_name))
    columns = [column[1] for column in cursor.fetchall() if column[1] != 'id']

    values = [input("Введите значение для {}: ".format(column))
              for column in columns]

    query = "INSERT INTO {} ({}) VALUES ({})".format(
        table_name, ', '.join(columns), ', '.join('?' * len(columns)))
    cursor.execute(query, values)
    conn.commit()
    print("Новая запись успешно добавлена.")


def view_records(cursor, table_name):
    cursor.execute("SELECT * FROM {}".format(table_name))
    records = cursor.fetchall()
    for record in records:
        print(record)


conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS money (
        id INTEGER PRIMARY KEY,
        value INTEGER
    )
''')

for i in range(1, 1001):
    cursor.execute("INSERT INTO money (value) VALUES (?)", (i,))
conn.commit()
print("1000 новых записей успешно добавлены в таблицу money.")

while True:
    print("\nВыберите таблицу для выполнения операций:")
    print("1. Clients")
    print("2. Accounts")
    print("3. Transactions")
    print("4. Employees")
    print("5. Loans")
    print("6. Money")
    print("7. Выйти")

    table_choice = input("Введите номер таблицы: ")

    if table_choice == '7':
        print("Программа завершена.")
        break

    tables = ['Clients', 'Accounts', 'Transactions',
              'Employees', 'Loans', 'money']
    table_name = tables[int(table_choice) -
                        1] if 1 <= int(table_choice) <= len(tables) else None

    if not table_name:
        print("Некорректный выбор таблицы. Попробуйте снова.")
        continue

    print("\nВыберите операцию для таблицы {}: ")
    print("1. Добавить новую запись")
    print("2. Просмотреть записи")
    print("3. Выйти из таблицы")

    operation_choice = input("Введите номер операции: ")

    if operation_choice == '1':
        add_record(conn, cursor, table_name)
    elif operation_choice == '2':
        view_records(cursor, table_name)
    elif operation_choice == '3':
        print("Выход из таблицы {}.".format(table_name))
    else:
        print("Некорректная операция. Попробуйте снова")

conn.close()
