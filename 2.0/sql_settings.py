import sqlite3

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()

cursor.execute("""
create table data
(
    login    text not null
        constraint data_pk
            primary key,
    password text not null
);
""")
cursor.execute("""
create unique index data_login_uindex
    on data (login);
""")
connection.commit()
connection.close()
