#!/usr/bin/env
"""
        Application for storing and managing contacts
"""

from views import AddressBookView

ab_view = AddressBookView()


def main():
    while True:
        print('Commands: 1 - List; 2 - Search; 3- Add; 4 - Delete; 0 - Exit')
        command = input(' ?')
        if command == '1':
            ab_view.display_contact_list()
        elif command == '2':
            ab_view.search_contact()
        elif command == '3':
            ab_view.create_new_contact()
        elif command == '4':
            ab_view.del_contact()
        elif command in {'0', 'q'}:
            break


if __name__ == '__main__':
    print(__doc__)
    main()
