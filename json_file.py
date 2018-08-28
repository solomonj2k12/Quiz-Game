import json

from flask import request

from gameplay import add_correct_text, add_incorrect_text


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

    if question_is_picture_question(question):
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
        previous_player["incorrect guesses"] = append_and_return_incorrect_guesses_string(
            previous_player)
        return_player_to_riddle_data(previous_player)
        return False
