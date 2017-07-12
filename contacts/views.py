#!/python

from models import Contact


class ContactView:
    """ Views for Contacts """

    prefix = '\n\t=== > '

    def _input_data(value_name, value_length=1):
        """ Control for input data length """

        while True:
            print(ContactView.prefix, value_name,
                  ' (min length - {})'.format(value_length))
            value = input(' ?')
            if len(value) >= value_length:
                return value

    def _contact_list_view(contact_list=[]):
        """ Dispaly table """

        print('-' * 111)
        print(':{:5}: {:^40} : {:^40} : {:^15} :'.format(
            'N', 'First Name', 'Last Name', 'Phone'))
        print('-' * 111)
        for k, contact in enumerate(contact_list):
            print(':{:5}: {:^40} : {:^40} : {:^15} :'.format(
                k + 1, *contact[1:]))
        print('-' * 111)

    def display_contact_list():
        """ Dispaly all contacts """
        cursor = Contact.get_contact_list()
        contact_list = cursor.fetchall()
        ContactView._contact_list_view(contact_list)
        return contact_list

    def add_contact():
        """ Add contact if not exist """

        first_name = ContactView._input_data('Enter First Name', 3)
        last_name = ContactView._input_data('Enter Last Name', 3)
        phone = ContactView._input_data('Enter Phone ', 3)
        contact = Contact(first_name, last_name, phone)
        if contact.is_contact():
            print(ContactView.prefix,
                  'Can not add contact. This contact is present in database.')
            return
        contact.save_contact()
        print(contact, ContactView.prefix, 'contact added')

    def del_contact():
        """ Delete contact is exist """

        contact_list = ContactView.display_contact_list(
        )  # display contact list for delete choose to
        if not contact_list:
            print(ContactView.prefix,
                  'Database is empty.')
            return
        pk = input('Enter contact number to delete ?')
        pk = int(pk) - 1 if pk.isdigit() else -1  # make 0-based
        if 0 <= pk <= len(contact_list) - 1:  # check is pk in range
            Contact.delete_contact(contact_list[pk][0])
            print(ContactView.prefix, 'Deleted')
            return
        print(ContactView.prefix, 'Number incorrect.')

    def search_contact():
        """ Search contact by name or phone and display """

        ss = ContactView._input_data('Enter string to search', 2)
        cursor = Contact.search_contact(ss)
        ContactView._contact_list_view(cursor.fetchall())
