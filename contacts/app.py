#!/python


from models import Contact




contact = Contact('sss', 'fff', 'fsdfsd')
contact.add_contact()

cursor = Contact.get_contact_list()

for row in cursor:
	print(row)