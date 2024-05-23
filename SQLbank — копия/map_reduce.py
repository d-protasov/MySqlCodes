import sqlite3
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk

# Функция для обработки данных через MapReduce


def map_function(value):
    # Здесь вы можете добавить вашу логику обработки данных в соответствии с MapReduce
    return value * value  # Пример: возводим каждое значение в квадрат

# Функция для получения и обработки данных из таблицы "money"


def process_data(value):
    return map_function(value)


# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Получаем данные из таблицы "money"
cursor.execute("SELECT * FROM money")
values = [row[0] for row in cursor.fetchall()]

# Используем ThreadPoolExecutor для многопоточной обработки данных
with ThreadPoolExecutor() as executor:
    result = list(executor.map(process_data, values))

# Закрываем соединение с базой данных
conn.close()

# Создаем GUI окно для отображения результатов
root = tk.Tk()
root.title("Результат работы MapReduce")

# Функция для отображения результатов в окне


def display_result():
    result_text.delete('1.0', tk.END)
    for idx, value in enumerate(result):
        result_text.insert(tk.END, f"Значение {
                           values[idx]} обработано как {value}\n")


result_text = tk.Text(root, height=15, width=40)
result_text.pack()

result_button = tk.Button(
    root, text="Показать результаты", command=display_result)
result_button.pack()

root.mainloop()
