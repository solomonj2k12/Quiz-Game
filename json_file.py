import json

from random import choice


from flask import request

from gametext import add_eliminated_text, add_correct_text, add_incorrect_text,add_quiz_master_text, add_question_text,  add_correct_answer_text



def dump_data(player_list):
    '''
    will wipe the player.json file, so that it is empty for new game
    '''
    
    with open("gamefiles/players.json", mode="w", encoding="utf-8") as riddle_data:
        json.dump(player_list, riddle_data)
        
def get_player_data():
    '''
    will return the players usernames in player.json
    '''
    
    with open("gamefiles/players.json", "r") as json_file:
        json_data = json.load(json_file)
        return json_data



def create_riddle_data(number_of_players):
    '''
    this creates the game data such as the lives, score, usernames and so on, 
    this is a key function for the game to work
    '''
    player_list = []
    for i in range(number_of_players):
        username = request.form["player-{0}-username".format(i + 1)]
        player_object = {
            "username": username,
            "lives": 3,
            "score": 0,
            "question": "",
            "last question correct": True,  
            "turn": False, 
            "previous": False,
            "answer": "",
            "no": i + 1,
            "incorrect guesses": ""
        }
        player_list.append(player_object)
    dump_data(player_list)
    
    
    
def set_player_turn():
    '''
    this dictakes who go it is in the game
    '''
   
    riddle_data = get_player_data()
    number_of_players = len(riddle_data)
    player_index = 0

    for player in riddle_data:
        player["previous"] = False

    for player in riddle_data:
        if player["turn"]:
            player["previous"] = True
            player_index = riddle_data.index(player)
            player["turn"] = False

    if player_index < number_of_players - 1:
        riddle_data[player_index + 1]["turn"] = True

    else:
        riddle_data[0]["turn"] = True

    dump_data(riddle_data)
    
def set_previous_answer():
    """
    this comes into play after the ppst, it will gets the answer
    entered into answer form and the player in players.json, 
    this information is converted into a list of lower case strings
    """
    
    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()

    previous_player = get_previous_player()
    previous_player["answer"] = user_answer_list

    return_player_to_riddle_data(previous_player)
    
def get_previous_player():
 
    '''
     returns the data in players.json with a
     value of True
    ''' 
    riddle_data = get_player_data()
    previous_player = {}

    for player in riddle_data:
        if player["previous"]:
            previous_player = player

    return previous_player
    
    
def return_player_to_riddle_data(player_to_return):
   
    riddle_data = get_player_data()
    player_index = 999

    for player in riddle_data:
        if player["no"] == player_to_return["no"]:
            player_index = riddle_data.index(player)

    riddle_data[player_index] = player_to_return
    dump_data(riddle_data)
    
def check_player_answer():
    '''
    this takes the users answer and check against the two keywords i have set,
    in the question files. if they answer correct they get the you got it correct output,
    or if they get it wrong it runs the else statement
    '''
   
    previous_player = get_previous_player()
    answer = previous_player["answer"]

    question = previous_player["question"]

    if quiz_question(question):
        keyword = question[3]
    else:
        keyword = question[2]

    if keyword in answer:
        add_correct_text("Correct!")
        previous_player["last question correct"] = True
        previous_player["incorrect guesses"] = ""
        return_player_to_riddle_data(previous_player)
        return True
    else:
        add_incorrect_text("Incorrect")
        previous_player["last question correct"] = False
        return_player_to_riddle_data(previous_player)
        return False
        


        
        
def question_correct(player):
   
    if player["last question correct"]:
        return True

    else:
        return False    
    
def quiz_question(question):
    """
    checks if question tuple is a picture
    question
    """
   
    if len(question) == 4:
        return True
    else:
        return False
        
def set_question_selector(current_score):
    '''
    this is a question selector, it will open only a certain question file, 
    depending on the users score, this makes the game get harder
    '''
    
    if current_score >= 12:
        return "Hard"
    elif current_score >= 7:
        return "Normal"
    elif current_score >= 5:
        return "Picture"
    else:
        return "Easy"
    
    
def adjust_score_and_lives(correct):
    '''
    this changes the user score and lives depending on how they answered
    '''
   
    previous_player = get_previous_player()

    if correct:
        previous_player["score"] += 1
    else:
        previous_player["lives"] -= 1

    return_player_to_riddle_data(previous_player)
    
    
def eliminate_zero_lives_user():
    '''
    this is the backend code for removing users from the game once they reached zero lives
    '''
   
    riddle_data = get_player_data()
    player_index = 999
    eliminated_user = False

    for player in riddle_data:
        if player["lives"] <= 0:
            player_index = riddle_data.index(player)
            add_eliminated_text(player)
            eliminated_user = player
            

    if player_index != 999:
        riddle_data.pop(player_index)
        dump_data(riddle_data)

    dump_data(riddle_data)
    return eliminated_user
    
    

    
def all_users_eliminated():
    '''
    depending on weather or not the player.json file is empty or not,
    it will will return false or true
    '''
    
    riddle_data = get_player_data()

    if len(riddle_data) > 0:
        return False
    else:
        return True
        
        
def start_question():
    '''
    this gets the first question from easy.txt and sends it to question_sheet.json
    '''
    
    question_list = [{"question": "sample_question"}]

    with open("gamefiles/questions_sheet.json", mode="w", encoding="utf-8") as f:
        json.dump(question_list, f)
        
def player_question():
    '''
    this sets the question for user but it depends weather or not they got there previous one correct or not,
    if they did it will display a new one otherwise it will be the same question as before
    '''
   
    active_user = get_active_user()

    if question_correct(active_user):
        selector = set_question_selector(active_user["score"])
        active_user["question"] = random_question_selector(selector)

    return_player_to_riddle_data(active_user)
    
    
def random_question_selector(selector):
    '''
    this function will select a question at random from my different question lists
    '''
   
    found_original_question = False
    questions_list = get_questions_answers_keywords(selector)

    while not found_original_question:

        random_question = choice(questions_list)

        if question_check(random_question):
            found_original_question = True

    return random_question
    


    
    
def get_questions_keywords(selector):
    """
    returns list of tuples in format of (question, answer, keyword)
    read from questions document. Question document selected by
    difficulty. Picture questions in format of (link, question, answer, keyword)
    """
    if selector == "Picture":
        return get_picture_question_list()

    else:
        with open("data/{}.txt".format(selector.lower()), "r") as questions_doc:
            doc_lines = questions_doc.read().splitlines()

        question_list = []

        for i in range(0, len(doc_lines), 4):
            question_list.append((doc_lines[i], doc_lines[i + 1], doc_lines[i + 2]))

        return question_list
    
    
def get_active_user():
    '''
    takes the user is player.json and gives them a value of truye
    '''
    
    active_user = {}
    riddle_data = get_player_data()

    for player in riddle_data:
        if player["turn"]:
            active_user = player

    return active_user
    
def ask_question():
    '''
    will ask the question to the user
    '''
   
    active_user = get_active_user()
    riddle_data = get_player_data()
    number_of_players = len(riddle_data)

    if number_of_players > 1:
        add_quiz_master_text("Its your go {}".format(active_user["username"]))

    if not question_correct(active_user):
        add_quiz_master_text("Why not have another go at it...")
  
    question = active_user["question"]

    if quiz_question(question):
        img_text = "<img src ='{}'>".format(question[0])
        add_question_text(img_text)
        add_question_text(question[1])
    else:
        add_question_text(question[0])
        
        
def get_question_sheet():
    '''
    opens the question sheet which contains the questions
    '''
    
    with open("gamefiles/questions_sheet.json", "r") as f:
        questions_sheet = json.load(f)
        return questions_sheet
        
        
def question_check(question_tuple):
    '''
    returns False if argument is in question_sheet.json,
    otherwise adds question to questions_sheet.json and returns True
    '''
   
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
        
def get_correct_answer(player):
   
    question_tuple = player["question"]
    if quiz_question(question_tuple):
        correct_answer = question_tuple[2]
    else:
        correct_answer = question_tuple[1]
        add_correct_answer_text(correct_answer)
        
def add_to_questions_sheet(question, questions_sheet):
    '''
    adds questions to the question sheet
    '''
    
    questions_sheet.append({"question": question[0]})

    with open("gamefiles/questions_sheet.json", mode="w", encoding="utf-8") as f:
        json.dump(questions_sheet, f)
        
def get_questions_answers_keywords(selector):
    '''
    checks to see if the users answers matches the set keyword
    '''
   
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
    '''
    returns a list tuple of picture questions
    each tuple consists of link, question, answer,
    keyword
    '''
   
    with open("data/pictures.txt") as pictures_doc:
        pictures_lines = pictures_doc.read().splitlines()

    pictures_question_list = []

    for i in range(0, len(pictures_lines), 5):
        pictures_question_list.append(("/static/img/{}".format(
            pictures_lines[i]), pictures_lines[i + 1], pictures_lines[i + 2], pictures_lines[i + 3]))

    return pictures_question_list

def add_to_leaderboard(player):
    '''
    this takes the players usernames and score and send it to the leaderboard data file so it can be used to create the leaderboard
    '''
   
    username = player["username"]
    score = player["score"]

    saved_score = {"username": username, "score": score}
    data = get_leaderboard_data()
    data.append(saved_score)

    send_leaderboard_data(data)
    
def send_leaderboard_data(data):
   
    with open("data/leaderboardData.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f)
        
        
def get_scores():
    '''
    this code will gather the usernames and score and use them to create the leaderboards
    '''
    
    data = get_leaderboard_data()
    score_data = sorted(data, reverse=True,
                         key=lambda k: k["score"])
    return score_data
    
  
def get_leaderboard_data():
   
    with open("data/leaderboardData.json", "r") as f:
        data = json.load(f)
        return data

        

        
