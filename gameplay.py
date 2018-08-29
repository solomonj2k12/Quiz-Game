from random import choice

from json_file import get_question_sheet, add_to_questions_sheet


def wipe_gamefiles(game_over=False):
  
    f = open("gamefiles/correct.txt", "r+")
    f.truncate()
    f.close()
    
    f = open("gamefiles/eliminated.txt", "r+")
    f.truncate()
    f.close()
    
    if not game_over:
        f = open("gamefiles/answer.txt", "r+")
        f.truncate()
        f.close()




def add_correct_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='correct'>{}</span>".format(text))


def add_incorrect_text(text):
   
    with open("gamefiles/correct.txt", "a") as f:
        f.writelines("<span class='incorrect'>{}</span>".format(text))
        

def add_eliminated_text(player):
   
    username = player["username"]
    text_to_write = "{} has been eliminated".format(username)
    with open("gamefiles/eliminated.txt", "a") as f:
        f.writelines(text_to_write)
        
def add_correct_answer_text(correct_answer):
   

    text_to_write = "The correct answer was: {0}<br>".format(correct_answer)
    with open("gamefiles/answer.txt", "a") as f:
        f.writelines(text_to_write)
        
        
def question_correct(player):
   
    if player["last question correct"]:
        return True

    else:
        return False    
        
        
def add_quiz_master_text(text):
    
    with open("gamefiles/quizmaster.txt", "a") as f:
        f.writelines("{}<br>".format(text))   
        
        
def add_incorrect_answers_text(player):
   
    if len(player["incorrect answers"]) > 0:
        text_to_write = "<span id='guesses-title'>Incorrect answers: </span> <span class='guesses'> {0} </span>".format(
            player["incorrect answers"])
        with open("gamefiles/incorrect_answers.txt", "a") as f:
            f.writelines(text_to_write)
            
def quiz_question(question):
   
    if len(question) == 4:
        return True
    else:
        return False
        
def set_question_selector(current_score):
    
    if current_score >= 10:
        return "Hard"
    elif current_score >= 5:
        return "Picture"
    elif current_score >= 5:
        return "Normal"
    else:
        return "Easy"
        
        
def random_question_selector(selector):
   
    found_original_question = False
    questions_list = get_questions_answers_keywords(selector)

    while not found_original_question:

        random_question = choice(questions_list)

        if question_check(random_question):
            found_original_question = True

    return random_question
    
    
def get_questions_answers_keywords(selector):
   
    if selector == "Picture":
        return get_picture_question_list()

    else:
        with open("data/{}.txt".format(selector.lower()), "r") as questions_doc:
            doc_lines = questions_doc.read().splitlines()

        question_list = []

        for i in range(0, len(doc_lines), 4):
            question_list.append((doc_lines[i], doc_lines[i + 1], doc_lines[i + 2]))

        return question_list
        
    
def get_picture_question_list():
   
    with open("data/pictures.txt") as pictures_doc:
        pictures_lines = pictures_doc.read().splitlines()

    pictures_question_list = []

    for i in range(0, len(pictures_lines), 5):
        pictures_question_list.append(("/static/img/{}".format(
            pictures_lines[i]), pictures_lines[i + 1], pictures_lines[i + 2], pictures_lines[i + 3]))

    return pictures_question_list
    
    
def question_check(question_tuple):
   
    questions_sheet = get_question_sheet()
    original_question = True

    for question in questions_sheet:
        if question["question"] == question_tuple[0]:
            original_question = False

    if not original_question:
        return False

    else:
        add_to_questions_sheet(question_tuple, questions_sheet)
        return True
        
        
def add_question_text(question):
    
    with open("gamefiles/question.txt", "a") as f:
        f.writelines("{}<br>".format(question))
        
        
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

    with open("gamefiles/answer.txt", "r") as f:
        answer_text = f.readlines()
        end_text_dictionary["answer text"] = answer_text

    with open("gamefiles/quizmaster.txt", "r") as f:
        host_text = f.readlines(
        end_text_dictionary["quizmaster text"] = quizmaster_text

    with open("gamefiles/question.txt", "r") as f:
        question_text = f.readlines()
        end_text_dictionary["question text"] = question_text

    with open("gamefiles/incorrect_answers.txt", "r") as f:
        incorrect_answers_text = f.readlines()
        end_text_dictionary["incorrect answers text"] = incorrect_answers_text

    with open("gamefiles/gameEnd.txt", "r") as f:
        game_end_text = f.readlines()
        end_text_dictionary["game over text"] = game_end_text

    return end_text_dictionary

    