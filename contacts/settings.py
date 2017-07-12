#!/python

import sqlite3

conn = sqlite3.connect('contact.db')

conn.execute("""create table if not exists CONTACT
    (ID	INT PRIMARY KEY NOT NULL,
     FIRST_NAME TEXT NOT NULL,
     LAST_NAME TEXT NOT NULL,
     PHONE CHAR(15));""")

conn.commit()
