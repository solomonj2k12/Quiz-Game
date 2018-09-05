import json

from random import choice


from flask import request

from gametext import add_eliminated_text, add_correct_text, add_incorrect_text, add_correct_answer_text, add_quiz_master_text, add_question_text



def dump_data(player_list):
    
    with open("gamefiles/players.json", mode="w", encoding="utf-8") as riddle_data:
        json.dump(player_list, riddle_data)
        
def get_player_data():
    
    with open("gamefiles/players.json", "r") as json_file:
        json_data = json.load(json_file)
        return json_data



def create_riddle_data(number_of_players):
    
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
    
    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()

    previous_player = get_previous_player()
    previous_player["answer"] = user_answer_list

    return_player_to_riddle_data(previous_player)
    
def get_previous_player():
  
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
        previous_player["incorrect guesses"] = return_incorrect_guesses(
            previous_player)
        return_player_to_riddle_data(previous_player)
        return False
        


        
        
def question_correct(player):
   
    if player["last question correct"]:
        return True

    else:
        return False    
        
        
  
        
        
def get_correct_answer(player):
   
    question_tuple = player["question"]
    if quiz_question(question_tuple):
        correct_answer = question_tuple[2]
    else:
        correct_answer = question_tuple[1]

    add_correct_answer_text(correct_answer)
    
    
def return_incorrect_guesses(player):
   
    incorrect_guesses = player["incorrect guesses"]
    last_guess = player["answer"]

    last_guess_string = " ".join(str(word) for word in last_guess)
    new_text = "{0}<br>{1}".format(incorrect_guesses, last_guess_string)
    return new_text
    
    
def quiz_question(question):
   
    if len(question) == 4:
        return True
    else:
        return False
        
def set_question_selector(current_score):
    
    if current_score >= 12:
        return "Hard"
    elif current_score >= 7:
        return "Normal"
    elif current_score >= 5:
        return "Picture"
    else:
        return "Easy"
    
    
def adjust_score_and_lives(correct):
   
    previous_player = get_previous_player()

    if correct:
        previous_player["score"] += 1
    else:
        previous_player["lives"] -= 1

    return_player_to_riddle_data(previous_player)
    
    
def eliminate_zero_lives_user():
   
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
    
'''    
def add_to_leaderboard(player):
   
    username = player["username"]
    score = player["score"]

    saved_score = {"username": username, "score": score}
    leaderboard_data = get_leaderboard_data()
    leaderboard_data.append(saved_score)

    send_leaderboard_data(leaderboard_data)
    
def send_leaderboard_data(leaderboard_data):
   
    with open("data/leaderboardData.json", mode="w", encoding="utf-8") as f:
        json.dump(leaderboard_data, f)
        
        
def get_scores():
    
    leaderboard_data = get_leaderboard_data()
    score_data = sorted(leaderboard_data, reverse=True,
                         key=lambda k: k["score"])
    return score_data
    
  
def get_leaderboard_data():
   
    with open("data/leaderboardData.json", "r") as f:
        leaderboard_data = json.load(f)
        return leaderboard_data
'''
    
def all_users_eliminated():
    
    
    riddle_data = get_player_data()

    if len(riddle_data) > 0:
        return False
    else:
        return True
        
        
def start_question():
    
    question_list = [{"question": "sample_question"}]

    with open("gamefiles/questions_sheet.json", mode="w", encoding="utf-8") as f:
        json.dump(question_list, f)
        
def player_question():
   
    active_user = get_active_user()

    if question_correct(active_user):
        selector = set_question_selector(active_user["score"])
        active_user["question"] = random_question_selector(selector)

    return_player_to_riddle_data(active_user)
    
    
def random_question_selector(selector):
   
    found_original_question = False
    questions_list = get_questions_answers_keywords(selector)

    while not found_original_question:

        random_question = choice(questions_list)

        if question_check(random_question):
            found_original_question = True

    return random_question
    


    
    
def get_questions_keywords(selector):
   
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
    
    active_user = {}
    riddle_data = get_player_data()

    for player in riddle_data:
        if player["turn"]:
            active_user = player

    return active_user
    
def ask_question():
   
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
    
    with open("gamefiles/questions_sheet.json", "r") as f:
        questions_sheet = json.load(f)
        return questions_sheet
        
        
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
        
def add_to_questions_sheet(question, questions_sheet):
    questions_sheet.append({"question": question[0]})

    with open("gamefiles/questions_sheet.json", mode="w", encoding="utf-8") as f:
        json.dump(questions_sheet, f)
        
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
    
        
        

        
def all_players_eliminated():
   
    riddle_data = get_player_data()

    if len(riddle_data) >= 0:
        return False
    else:
        return True
