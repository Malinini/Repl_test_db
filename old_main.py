import sqlite3
import datetime


def insert_db(ins):
    con = sqlite3.connect('test_db.db')
    cur = con.cursor()
    cur.execute('INSERT INTO birthday(first_name, second_name, date_b) VALUES (?, ?, ?);', ins)
    name, second_name, date = ins
    con.commit()
    con.close()
    return print(f'{name} {second_name} записан в базу данных с ДР {date}')


def view_db():
    con = sqlite3.connect('test_db.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM birthday')
    result_s = (cur.fetchall())
    con.close()
    return result_s


def search_db(what_search):
    con = sqlite3.connect('test_db.db')
    cur = con.cursor()
    if len(what_search) == 1:  # Если нашел одного
        cur.execute(f'''SELECT id, first_name, second_name, date_b 
                    FROM birthday 
                    WHERE first_name IS "{what_search[0]}" OR second_name IS "{what_search[0]}";''')
        result_s = cur.fetchall()
    else:  # Если нашел много
        cur.execute(f'''SELECT id, first_name, second_name, date_b 
                   FROM birthday 
                   WHERE (first_name IS "{what_search[0]}" OR second_name IS "{what_search[0]}") 
                   AND (first_name IS "{what_search[1]}" OR second_name IS "{what_search[1]}");''')
        result_s = cur.fetchall()
    if len(result_s) == 0:
        print('Таких еще нет в базе')
    con.close()
    return result_s


def view_search(search_result):
    for row in search_result:
        date_obj = datetime.datetime.strptime(row[3], '%d.%m.%Y')
        today = datetime.date.today()
        vozrast = today.year - date_obj.year - ((today.month, today.day) < (date_obj.month, date_obj.day))
        print(f'{row[1]} {row[2]} родился {row[3]} возраст {vozrast}')


def search_nestrog(what_search):
    new_search_list = []
    for word in what_search:
        word_len = len(word)
        if word_len > 3:
            marg = (word_len - 3) // 2
            new_word = word[:-2]

        else:
            new_word = word[0:2]
        new_search_list.append(new_word)
    con = sqlite3.connect('test_db.db')
    cur = con.cursor()
    if len(new_search_list) == 1:  # Если нашел одного
        cur.execute(f'''SELECT id, first_name, second_name, date_b 
        FROM birthday 
        WHERE first_name LIKE "{'%' + new_search_list[0] + '%'}" OR second_name LIKE "{'%' + new_search_list[0] + '%'}";''')
        result_s = cur.fetchall()
    else:  # Если нашел много
        cur.execute(f'''SELECT id, first_name, second_name, date_b 
        FROM birthday 
        WHERE first_name LIKE "{'%' + new_search_list[0] + '%'}" OR second_name LIKE "{'%' + new_search_list[0] + '%'}" OR first_name LIKE "{'%' + new_search_list[1] + '%'}" OR second_name LIKE "{'%' + new_search_list[1] + '%'}";''')
        result_s = cur.fetchall()
    if len(result_s) == 0:
        print('Таких еще нет в базе')
    con.close()
    return result_s


while True:

    command = input('введи команду: ')

    if command == 'add':
        date = str.title(input('введи Имя Фамилию и дату: '))
        insert = tuple(date.split())
        name, second_name, date_b = insert

        if len(search_db(insert)) > 0:
            print('Такой уже есть в базе')
        else:
            insert_db(insert)

    elif command == 'show':
        show = view_db()
        view_search(show)
    elif command == 'search':
        search = str.title(input('кого ищем: '))
        search_list = search.split();
        result = search_db(search_list)
        view_search(result)

    elif command == 'sos':
        new_search = str.title(input('кого ищем (не строго): '))
        result = search_nestrog(new_search.split())
        view_search(result)
    else:
        break
