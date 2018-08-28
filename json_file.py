import json

from flask import request

from gameplay import add_correct_text, add_incorrect_text, add_eliminated_text,  add_correct_answer_text


def dump_data(player_list):
  
    with open("gamefiles/players.json", mode="w", encoding="utf-8") as json_data:
        json.dump(player_list, json_data)
        
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
            add_to_leaderboard(player)
            player_index = riddle_data.index(player)
            add_eliminated_text(player)
            eliminated_user = player
            

    if player_index != 999:
        riddle_data.pop(player_index)
        dump_data(riddle_data)

    dump_data(riddle_data)
    return eliminated_user
    
def add_to_leaderboard(player):
   
    username = player["username"]
    score = player["score"]

    saved_score = {"username": username, "score": score}
    leaderboard_data = get_leaderboard_data()
    leaderboard_data.append(saved_score)

    post_leaderboard_data(leaderboard_data)
    
def all_users_eliminated():
    
    riddle_data = get_player_data()

    if len(riddle_data) > 0:
        return False
    else:
        return True

