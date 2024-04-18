
def read(users: list[dict])->None:
    for user in users[1:]:
        print(f'Twój znajomy {user["name"]} opublikował: {user["posts"]}')

def create_user(users:list[dict])->None:
    name: str = input("Podaj imię użytkownika: ")
    surname: str = input("Podaj nazwisko użytkownika: ")
    posts: int = int(input("Podaj liczbę postów użytkownika: "))
    user: dict = {"name": name, "surname": surname, "posts": posts}
    users.append(user)
