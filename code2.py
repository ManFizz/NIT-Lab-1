import sqlite3

con = sqlite3.connect("library.sqlite")  # создаем базу данных и устанавливаем соединение с ней

cursor = con.cursor()  # создаем курсор
cursor.execute('''
 SELECT 
 title,
 publisher_name,
 year_publication
 FROM book 
 JOIN genre USING (genre_id)
 JOIN publisher USING (publisher_id)
 WHERE genre_name = :p_genre AND year_publication > :p_year
''', {"p_genre": "Детектив", "p_year": 2016})  # выбираем и выводим записи из таблиц author, reader
print(cursor.fetchall())

con.close()  # закрываем соединение с базой
