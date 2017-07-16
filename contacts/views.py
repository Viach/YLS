from models import Contact, AddressBook

ab = AddressBook()


class BaseView:
    def __init__(self):
        self.prefix = '\n\t=== > '
        self.value_length = 1

    def _input_data(self, value_name, value_length):
        """ Control for input data length """

        while True:
            print(self.prefix, value_name,
                  ' (min length - {})'.format(value_length))
            value = input(' ?')
            if len(value) >= value_length:
                return value


class ContactView(BaseView):
    def add_contact(self):
        first_name = self._input_data('Enter First Name', 3)
        last_name = self._input_data('Enter Last Name', 3)
        phone = self._input_data('Enter Phone ', 3)
        contact = Contact(first_name, last_name, phone)
        return contact


class AddressBookView(BaseView):
    """ Views for Contacts """

    @staticmethod
    def _contact_list_view(contact_list):
        """ Display table """

        print('-' * 111)
        print(':{:5}: {:^40} : {:^40} : {:^15} :'.format(
            'N', 'First Name', 'Last Name', 'Phone'))
        print('-' * 111)
        for k, contact in enumerate(contact_list):
            print(':{:5}: {:^40} : {:^40} : {:^15} :'.format(
                k + 1, *contact[1:]))
        print('-' * 111)

    def display_contact_list(self):
        """ Display all contacts """
        contact_list = ab.get_contact_list()
        self._contact_list_view(contact_list)
        return contact_list

    def create_new_contact(self):
        """ Add contact if not exist """
        contact_view = ContactView()
        contact = contact_view.add_contact()
        if ab.is_contact(contact):
            print(self.prefix,
                  'Can not add contact. This contact is present in database.')
            return
        ab.save_contact(contact)

    def del_contact(self):
        """ Delete contact if exist """

        contact_list = self.display_contact_list()  # display contact list for delete choose to
        if not contact_list:
            print(self.prefix,
                  'Database is empty.')
            return
        pk = input('Enter contact number to delete ?')
        pk = int(pk) - 1 if pk.isdigit() else -1  # make 0-based
        if 0 <= pk <= len(contact_list) - 1:  # check is pk in range
            contact = Contact(*contact_list[pk][1:])
            ab.delete_contact(contact)
            print(self.prefix, 'Deleted')
        else:
            print(self.prefix, 'Number incorrect.')

    def search_contact(self):
        """ Search contact by name or phone and display """

        ss = self._input_data('Enter string to search', 2)
        contact_list = ab.search_contact(ss)
        self._contact_list_view(contact_list)
