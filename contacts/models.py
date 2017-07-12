#!/python
from settings import conn


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

    @staticmethod
    def get_contact_list():
        cursor = conn.execute("""
            select * from CONTACT; 
            """)
        return cursor

    @staticmethod
    def delete_contact(pk):
        conn.execute("""  
            DELETE FROM CONTACT WHERE ID=?;
            """, (pk,))
        conn.commit()

    @staticmethod
    def search_contact(ss):  # ss is string_to_seacrh 
        cursor = conn.execute("""  
            SELECT * FROM CONTACT WHERE 
            FIRST_NAME LIKE ?  OR LAST_NAME LIKE ? OR PHONE LIKE ?; 
            """, ('%{}%'.format(ss), '%{}%'.format(ss), '%{}%'.format(ss),))
        return cursor

    def is_contact(self):
        cursor = conn.execute("""  
            SELECT * FROM CONTACT WHERE FIRST_NAME=? AND LAST_NAME=? LIMIT 1;
            """, (self.first_name, self.last_name))
        return len(cursor.fetchall()) == 1

    def save_contact(self):
        cursor = conn.execute("""  
            SELECT ID FROM CONTACT ORDER BY id DESC LIMIT 1;
            """)  # get last id from database
        max_id_row = [row for row in cursor]
        pk = max_id_row[0][0] + 1 if len(max_id_row) else 1
        conn.execute("""
            INSERT INTO CONTACT VALUES (?, ?, ?, ?);
            """, (pk, self.first_name, self.last_name, self.phone))
        conn.commit()
