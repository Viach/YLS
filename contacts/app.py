#!/python


from models import Contact



cursor = Contact._get_last_pk()
print(cursor)

contact = Contact('sss', 'fff', 'fsdfsd')
contact.add_contact()

cursor = Contact.get_contact_list()

for row in cursor:
	print(row)