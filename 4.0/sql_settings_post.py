import sqlite3

connection = sqlite3.connect("posts.sqlite")
cursor = connection.cursor()

cursor.execute("""
    create table data
    (
    id integer not null constraint data_pk primary key autoincrement,
    autor text not null,
    text text not null,
    tegs text not null
);
""")
cursor.execute("""
create unique index data_login_uindex on data (id);
""")
connection.commit()
connection.close()
