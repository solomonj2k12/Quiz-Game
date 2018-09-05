def add_eliminated_text(player):
   
    username = player["username"]
    text_to_write = "{} has been eliminated".format(username)
    with open("gamefiles/eliminated.txt", "a") as f:
        f.writelines(text_to_write)