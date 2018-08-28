def wipe_gamefiles(game_over=False):
  
    f = open("active-game-files/correct.txt", "r+")
    f.truncate()
    f.close()




def add_correct_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='correct'>{}</span>".format(text))


def add_incorrect_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='incorrect'>{}</span>".format(text))