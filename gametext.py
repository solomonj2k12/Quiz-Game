def add_eliminated_text(player):
    '''
    displays that a user got eliminated
    '''
    username = player["username"]
    text_to_write = "{} has been eliminated".format(username)
    with open("gamefiles/eliminated.txt", "a") as f:
        f.writelines(text_to_write)
        
def add_correct_text(text):
    '''
    displays they got the question correct
    '''
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='correct'>{}</span>".format(text))
        
def add_incorrect_text(text):
    '''
    displays they got the question incorrect
    '''
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='incorrect'>{}</span>".format(text))
        

def add_quiz_master_text(text):
    
    
    with open("gamefiles/quizmaster.txt", "a") as f:
        f.writelines("{}<br>".format(text)) 
        
def add_correct_answer_text(correct_answer):
    """
    writes the correct answer to the player's
    question in answer.txt
    """

    text_to_write = "The correct answer was: {0}<br>".format(correct_answer)
    with open("active-game-files/answer.txt", "a") as f:
        f.writelines(text_to_write)
        
        
def add_question_text(question):
    '''
    writes the question into the file
    '''
    with open("gamefiles/question.txt", "a") as f:
        f.writelines("{}<br>".format(question))
        