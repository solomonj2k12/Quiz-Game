def add_eliminated_text(player):
   
    username = player["username"]
    text_to_write = "{} has been eliminated".format(username)
    with open("gamefiles/eliminated.txt", "a") as f:
        f.writelines(text_to_write)
        
def add_correct_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='correct'>{}</span>".format(text))
        
def add_incorrect_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='incorrect'>{}</span>".format(text))
        


        
def add_correct_answer_text(correct_answer):
   

    text_to_write = "The correct answer was: {0}<br>".format(correct_answer)
    with open("gamefiles/answer.txt", "a") as f:
        f.writelines(text_to_write)
        
def add_quiz_master_text(text):
    
    with open("gamefiles/quizmaster.txt", "a") as f:
        f.writelines("{}<br>".format(text)) 
        
        
def add_question_text(question):
    
    with open("gamefiles/question.txt", "a") as f:
        f.writelines("{}<br>".format(question))
        