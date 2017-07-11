from settings import conn


class Contact:

    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __str__(self):
        return "Name:{0} {1}\nPhone:{2}".format(self.first_name, self.last_name, self.phone)

    @staticmethod
    def get_contact_list():
        row = conn.execute("""
    		select * from CONTACT; 
    		""")
        return row


    def add_contact(self):
    	cursor = conn.execute("""
    		SELECT ID FROM CONTACT ORDER BY id DESC LIMIT 1;
    		""")
    	pk = [row for row in cursor][0][0]
    	print(pk)
    	pk += 1
    	conn.execute("""
    		insert into CONTACT values ({}, "Melksham{}{}", "{}", "{}");
    		""".format(pk, pk, self.first_name, self.last_name, self.phone))
    	conn.commit()
