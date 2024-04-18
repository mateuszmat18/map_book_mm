from utils.crud import read, create_user, search
from models.data import users


if __name__ == '__main__':

    print(f"Witaj {users[0]['name']}!")
    while True:
        print("Menu:")
        print("0. Zakończ program:")
        print("1.Pokaż co u znajomych: ")
        print("2.Dodaj znajomego: ")
        print("3.Pokaż co u znajomych: ")
        menu_option: str = input("Wybierz dostępną funkcję z menu: ")
        if menu_option == "0":
            break
        if menu_option == "1":
            read(users)
        if menu_option == "2":
            create_user(users)
        if menu_option == "3":
            search(users)





