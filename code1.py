import sqlite3

con = sqlite3.connect("library.sqlite")  # создаем базу данных и устанавливаем соединение с ней

f_damp = open('library.db', 'r', encoding='utf-8-sig')  # открываем файл с дампом базой данных
damp = f_damp.read()  # читаем данные из файла
f_damp.close()  # закрываем файл с дампом

con.executescript(damp)  # запускаем запросы
con.commit()  # сохраняем информацию в базе данны

cursor = con.cursor()  # создаем курсор
# выбираем и выводим записи из таблиц author, reader
cursor.execute("SELECT * FROM author")
print(cursor.fetchall())
cursor.execute("SELECT * FROM reader")
print(cursor.fetchall())

# закрываем соединение с базой
con.close()
