import sqlite3

conn = sqlite3.connect('contact.db')
#conn.execute('drop table if exists ADDRESSBOOK;')
conn.execute("""create table if not exists CONTACT
	(ID	INT PRIMARY KEY NOT NULL,
	 FIRST_NAME TEXT NOT NULL,
	 LAST_NAME TEXT NOT NULL,
	 PHONE CHAR(15));""")
#conn.execute("""insert into ADDRESSBOOK values (1, "Melksham", "SN12", "23144321");""")
 
conn.commit()