import sqlite3

con = sqlite3.connect("store.sqlite")  # создаем базу данных и устанавливаем соединение с ней

# инициализация бд
f_damp = open('store.db', 'r', encoding='utf-8-sig')  # открываем файл с дампом базой данных
damp = f_damp.read()  # читаем данные из файла
f_damp.close()  # закрываем файл с дампом

con.executescript(damp)  # запускаем запросы
con.commit()  # сохраняем информацию в базе данны

# работа с бд
cursor = con.cursor()  # создаем курсор

# 1
cursor.execute('''SELECT DISTINCT c.name_client
FROM client c
JOIN buy b ON c.client_id = b.client_id
JOIN buy_book bb ON b.buy_id = bb.buy_id
JOIN book bk ON bb.book_id = bk.book_id
JOIN author a ON bk.author_id = a.author_id
WHERE bk.title = 'Поэмы' AND a.name_author = 'Пушкин А.С.'
ORDER BY c.name_client DESC;''')
print(cursor.fetchall())

# 2
cursor.execute('''SELECT c.name_client, COALESCE(SUM(bb.amount), 0) AS Количество
FROM client c
LEFT JOIN buy b ON c.client_id = b.client_id
LEFT JOIN buy_book bb ON b.buy_id = bb.buy_id
GROUP BY c.name_client
ORDER BY Количество DESC, c.name_client;''')
print(cursor.fetchall())

# 3
cursor.execute('''WITH RankedBooks AS (
    SELECT
        b.title AS book1,
        b.author_id,
        b.price AS price1,
        LEAD(b.title) OVER (PARTITION BY b.author_id ORDER BY b.price DESC) AS book2,
        LEAD(b.price) OVER (PARTITION BY b.author_id ORDER BY b.price DESC) AS price2,
        COUNT(*) OVER (PARTITION BY b.author_id) AS book_count
    FROM
        book b
)

SELECT
    a.name_author AS Автор,
    r.book1 || '. ' || r.book2 AS Книги,
    ROUND(((r.price1 + r.price2) * 0.75), 2) AS Цена
FROM
    RankedBooks r
JOIN
    author a ON r.author_id = a.author_id
WHERE
    r.book2 IS NOT NULL AND r.book_count >= 2;''')
print(cursor.fetchall())

# 4
cursor.execute('''UPDATE book
SET price = 
    CASE
        WHEN amount < (SELECT AVG(amount) FROM book) THEN
            FLOOR(price) + 0.99
        ELSE
            CEIL(price) + 0.99
    END;''')
cursor.execute("SELECT * FROM book")
print(cursor.fetchall())

# 5
cursor.execute('''WITH RankedBooks AS (
    SELECT
        b.title AS book1,
        b.author_id,
        b.price AS price1,
        LEAD(b.title) OVER (PARTITION BY b.author_id ORDER BY b.price DESC) AS book2,
        LEAD(b.price) OVER (PARTITION BY b.author_id ORDER BY b.price DESC) AS price2
    FROM
        book b
)

SELECT
    a.name_author AS Автор,
    r.book1 || '. ' || r.book2 AS Книги,
    ROUND(((r.price1 + r.price2) * 0.75), 2) AS Цена
FROM
    RankedBooks r
JOIN
    author a ON r.author_id = a.author_id
WHERE
    r.book2 IS NOT NULL;''')
print(cursor.fetchall())

# закрываем соединение с базой
con.close()
