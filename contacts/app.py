#!/python
"""
        Application for storing and managing contacts

"""

from views import ContactView


def main():
    while True:
        print('Commands: 1 - List; 2 - Search; 3- Add; 4 - Delete; 0 - Exit')
        command = input(' ?')
        if command == '1':
            ContactView.display_contact_list()
        elif command == '2':
            ContactView.search_contact()
        elif command == '3':
            ContactView.add_contact()
        elif command == '4':
            ContactView.del_contact()
        elif command in {'0', 'q'}:
            break


if __name__ == '__main__':
    print(__doc__)
    main()
