import sqlite3
from datetime import datetime

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('real_estate_db.db')
cursor = conn.cursor()

# Функция для создания таблиц


def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        passport_number TEXT UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        property_id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_type TEXT,
        address TEXT,
        price REAL,
        area REAL,
        status TEXT CHECK(status IN ('for sale', 'sold')) DEFAULT 'for sale',
        client_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER,
        sale_price REAL,
        commission_rate REAL,
        transaction_date TEXT,
        FOREIGN KEY (property_id) REFERENCES properties(property_id)
    )
    ''')

# Функция для вставки данных о клиенте


def insert_client(first_name, last_name, passport_number):
    try:
        cursor.execute('''
        INSERT INTO clients (first_name, last_name, passport_number) VALUES (?, ?, ?)
        ''', (first_name, last_name, passport_number))
        conn.commit()
        print("Клиент добавлен")
    except sqlite3.IntegrityError:
        print("Клиент с таким номером паспорта уже существует")

# Функция для вставки данных о недвижимости


def insert_property(property_type, address, price, area, client_id):
    cursor.execute('''
    INSERT INTO properties (property_type, address, price, area, client_id) VALUES (?, ?, ?, ?, ?)
    ''', (property_type, address, price, area, client_id))
    conn.commit()
    print("Недвижимость добавлена")

# Функция для поиска клиента


def search_client(passport_number=None, first_name=None, last_name=None):
    if passport_number:
        cursor.execute('''
        SELECT * FROM clients WHERE passport_number=?
        ''', (passport_number,))
    elif first_name and last_name:
        cursor.execute('''
        SELECT * FROM clients WHERE first_name=? AND last_name=?
        ''', (first_name, last_name))
    else:
        return None
    return cursor.fetchone()

# Функция для поиска недвижимости


def search_property(price=None, location=None, area=None):
    query = 'SELECT * FROM properties WHERE 1=1'
    params = []
    if price:
        query += ' AND price<=?'
        params.append(price)
    if location:
        query += ' AND address LIKE ?'
        params.append(f'%{location}%')
    if area:
        query += ' AND area>=?'
        params.append(area)
    cursor.execute(query, params)
    return cursor.fetchall()

# Функция для вставки данных о транзакции


def insert_transaction(property_id, sale_price, commission_rate):
    cursor.execute('''
    INSERT INTO transactions (property_id, sale_price, commission_rate, transaction_date)
    VALUES (?, ?, ?, ?)
    ''', (property_id, sale_price, commission_rate, datetime.now().strftime('%Y-%m-%d')))
    cursor.execute('''
    UPDATE properties SET status='sold' WHERE property_id=?
    ''', (property_id,))
    conn.commit()
    print("Транзакция добавлена")

# Функция для определения прибыли


def calculate_profit(start_date, end_date):
    cursor.execute('''
    SELECT SUM(sale_price * commission_rate / 100) FROM transactions
    WHERE transaction_date BETWEEN ? AND ?
    ''', (start_date, end_date))
    return cursor.fetchone()[0]

# Функция для получения списка самых популярных предложений


def get_popular_properties():
    cursor.execute('''
    SELECT property_id, COUNT(*) as count FROM transactions
    GROUP BY property_id ORDER BY count DESC LIMIT 5
    ''')
    return cursor.fetchall()

# Диалог с пользователем


def main():
    create_tables()

    while True:
        print("\nМеню:")
        print("1. Добавить клиента")
        print("2. Добавить недвижимость")
        print("3. Найти клиента")
        print("4. Найти недвижимость")
        print("5. Добавить транзакцию")
        print("6. Рассчитать прибыль")
        print("7. Самые популярные предложения")
        print("8. Выйти")

        choice = input("Выберите пункт меню: ")

        if choice == '1':
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            passport_number = input("Введите номер паспорта: ")
            insert_client(first_name, last_name, passport_number)

        elif choice == '2':
            property_type = input("Введите тип недвижимости: ")
            address = input("Введите адрес: ")
            price = float(input("Введите цену: "))
            area = float(input("Введите площадь: "))
            client_id = int(input("Введите ID клиента: "))
            insert_property(property_type, address, price, area, client_id)

        elif choice == '3':
            search_type = input("Поиск по (1: номеру паспорта, 2: ФИО): ")
            if search_type == '1':
                passport_number = input("Введите номер паспорта: ")
                client = search_client(passport_number=passport_number)
            elif search_type == '2':
                first_name = input("Введите имя: ")
                last_name = input("Введите фамилию: ")
                client = search_client(
                    first_name=first_name, last_name=last_name)

            if client:
                print("Результат поиска:", client)
            else:
                print("Клиент не найден")

        elif choice == '4':
            price = input(
                "Введите максимальную цену (оставьте пустым для пропуска): ")
            location = input(
                "Введите расположение (оставьте пустым для пропуска): ")
            area = input(
                "Введите минимальную площадь (оставьте пустым для пропуска): ")

            price = float(price) if price else None
            area = float(area) if area else None

            properties = search_property(
                price=price, location=location, area=area)
            for prop in properties:
                print(prop)

        elif choice == '5':
            property_id = int(input("Введите ID недвижимости: "))
            sale_price = float(input("Введите цену продажи: "))
            commission_rate = float(input("Введите процент комиссии: "))
            insert_transaction(property_id, sale_price, commission_rate)

        elif choice == '6':
            start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
            end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
            profit = calculate_profit(start_date, end_date)
            print("Прибыль за выбранный период:", profit)

        elif choice == '7':
            properties = get_popular_properties()
            for prop in properties:
                print("ID недвижимости:", prop[0],
                      "Количество транзакций:", prop[1])

        elif choice == '8':
            print("Выход из программы")
            break

        else:
            print("Некорректный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
    conn.close()
