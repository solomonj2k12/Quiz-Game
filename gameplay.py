from random import choice


def wipe_gamefiles(game_end=False):
        """
        wipes all game text files when
        game is over.
        """
        f = open("gamefiles/gameEnd.txt", "r+")
        f.truncate()
        f.close()
        
        f = open("gamefiles/eliminated.txt", "r+")
        f.truncate()
        f.close()
        
        f = open("gamefiles/correct.txt", "r+")
        f.truncate()
        f.close()
        
        f = open("gamefiles/quizmaster.txt", "r+")
        f.truncate()
        f.close()
        
        if not game_end:
        
            f = open("gamefiles/question.txt", "r+")
            f.truncate()
            f.close()
        
def game_end_text():
  
    with open("gamefiles/gameEnd.txt", "a") as f:
        f.writelines("Game Over Thanks for playing")
        
        
def get_end_text():
   
    end_text_dictionary = {}

    with open("gamefiles/correct.txt", "r") as f:
        correct_text = f.readlines()
        end_text_dictionary["correct text"] = correct_text

    with open("gamefiles/eliminated.txt", "r") as f:
        eliminated_text = f.readlines()
        end_text_dictionary["eliminated text"] = eliminated_text

    with open("gamefiles/quizmaster.txt", "r") as f:
        quizmaster_text = f.readlines()
        end_text_dictionary["quizmaster text"] = quizmaster_text
    
    with open("gamefiles/question.txt", "r") as f:
        question_text = f.readlines()
        end_text_dictionary["question text"] = question_text

    with open("gamefiles/gameEnd.txt", "r") as f:
        game_end_text = f.readlines()
        end_text_dictionary["game over text"] = game_end_text

    return end_text_dictionary

    
    