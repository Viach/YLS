import sqlite3
from os import path

SQL_FILENAME = 'addresbook.sqlite'


class Contact:
    """ Class Contact """

    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __str__(self):
        return "Name:{0} {1}\nPhone:{2}".format(self.first_name,
                                                self.last_name,
                                                self.phone)


class AddressBook:
    """ Class AddressBook """

    def __init__(self):
        if not path.exists(SQL_FILENAME):
            self.conn = sqlite3.connect(SQL_FILENAME)
            self.conn.execute("""CREATE TABLE IF NOT EXISTS CONTACT 
                            (ID	INTEGER PRIMARY KEY AUTOINCREMENT ,
                            FIRST_NAME CHAR(150),
                            LAST_NAME CHAR(150),
                            PHONE CHAR(15));
                            """)
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(SQL_FILENAME)

    def __str__(self):
        return "Address Book. Total contacts : {}".format(len(self.get_contact_list()))

    def get_contact_list(self):
        cursor = self.conn.execute("""
            SELECT * FROM CONTACT; 
            """)
        contact_list = cursor.fetchall()
        return contact_list

    def delete_contact(self, contact):
        self.conn.execute("""  
            DELETE FROM CONTACT WHERE FIRST_NAME = ?  AND LAST_NAME = ? AND PHONE = ?; 
            """, (contact.first_name, contact.last_name, contact.phone))
        self.conn.commit()

    def search_contact(self, ss):  # ss is string_to_seacrh
        cursor = self.conn.execute("""  
            SELECT * FROM CONTACT WHERE 
            FIRST_NAME LIKE ?  OR LAST_NAME LIKE ? OR PHONE LIKE ?; 
            """, ('%{}%'.format(ss), '%{}%'.format(ss), '%{}%'.format(ss),))
        return cursor.fetchall()

    def is_contact(self, contact):
        cursor = self.conn.execute("""  
            SELECT * FROM CONTACT WHERE FIRST_NAME=? AND LAST_NAME=? LIMIT 1;
            """, (contact.first_name, contact.last_name))
        return len(cursor.fetchall()) == 1

    def save_contact(self, contact):
        self.conn.execute("""
            INSERT INTO CONTACT ('first_name', 'last_name', 'phone') VALUES (?, ?, ?);
            """, (contact.first_name, contact.last_name, contact.phone))
        self.conn.commit()
