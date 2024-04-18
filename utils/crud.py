
def read(users: list[dict])->None:
    for user in users[1:]:
        print(f'Twój znajomy {user["name"]} opublikował: {user["posts"]}')
